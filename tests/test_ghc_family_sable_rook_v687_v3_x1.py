from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v687-v3"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "71e94d1699eea013c82bef0b7a7e081ac6e43c8c"
BRANCH = "codex/GHC-Family/sable-rook-v687-v3-full-tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, encoding="utf-8", capture_output=True).stdout.strip()


class SableRookV687V3X1Tests(unittest.TestCase):
    def test_01_exact_source_and_branch(self):
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE)
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_02_planning_only(self):
        truth = load(X1 / "phase-truth.json")
        self.assertEqual(truth["state"], "PLANNING_ONLY")
        self.assertFalse(truth["implementation_started"])
        self.assertEqual(truth["observed_new_execution_outcomes"], 0)
        self.assertEqual(truth["packages_installed"], 0)
        self.assertFalse((BASE / "x2").exists())

    def test_03_source_receipts(self):
        source = load(X1 / "source-verification.json")
        self.assertTrue(source["baton_read_through_eof"])
        self.assertEqual(source["baton_lines"], 6583)
        self.assertEqual(source["source_manifest_bindings_replayed"], 743)
        self.assertEqual(source["source_content_seal_targets_replayed"], 36)
        self.assertEqual(source["manifest_and_seal_failures"], 0)
        self.assertEqual(source["canonical_replays"], 0)

    def test_04_exact_proposal_counts(self):
        proposals = load(X1 / "new-proposals.json")
        self.assertEqual(len(proposals["proposals"]), 200)
        self.assertEqual(proposals["counts"]["mutations_preregistered"], 1000)

    def test_05_proposal_required_fields(self):
        required = {"id", "title", "semantic_distinction", "operation", "pillar", "practice", "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition", "input", "expected_output", "mutations"}
        for row in load(X1 / "new-proposals.json")["proposals"]:
            self.assertTrue(required <= set(row))
            self.assertEqual(len(row["mutations"]), 5)

    def test_06_proposal_uniqueness(self):
        rows = load(X1 / "new-proposals.json")["proposals"]
        self.assertEqual(len({row["id"] for row in rows}), 200)
        self.assertEqual(len({row["title"] for row in rows}), 200)
        self.assertEqual(len({(row["operation"], json.dumps(row["input"], sort_keys=True)) for row in rows}), 200)
        novelty = load(X1 / "novelty-review.json")
        self.assertEqual(novelty["exact_title_collisions"], [])
        self.assertEqual(novelty["declared_chain_after"], 14430)

    def test_07_inherited_zero_credit(self):
        inherited = load(X1 / "inherited-selection.json")
        self.assertEqual(inherited["count"], 200)
        self.assertEqual(inherited["execution_credit"], 0)
        self.assertEqual(inherited["novelty_credit"], 0)

    def test_08_expected_outcomes(self):
        outcomes = load(X1 / "expected-outcomes.json")
        self.assertEqual(outcomes["counts"], {"completed": 160, "represented": 20, "open_gap": 10, "exact_gate": 10})
        self.assertEqual(set(outcomes["allowed_labels"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_09_portfolio_counts(self):
        plan = load(X1 / "portfolio-plan.json")
        self.assertEqual(len(plan["safe"]), 300)
        self.assertEqual(len(plan["candidates"]), 250)
        self.assertEqual(len(plan["clean_fix_refine"]), 300)
        self.assertEqual(len(plan["exact"]), 50)
        self.assertEqual(len(plan["blocked"]), 30)

    def test_10_held_packets(self):
        plan = load(X1 / "portfolio-plan.json")
        self.assertTrue(all(row["state"] == "HELD_UNEXECUTED" for row in plan["exact"] + plan["blocked"]))

    def test_11_skill_runner_plan(self):
        plan = load(X1 / "skill-runner-plan.json")
        self.assertEqual(len(plan["skills"]), 10)
        self.assertEqual(len(plan["runners"]), 10)
        self.assertEqual(len(plan["next_owner_skill_ideas"]), 10)
        self.assertEqual(len(plan["next_owner_runner_ideas"]), 10)
        self.assertTrue(all(not row["initialized"] for row in plan["skills"]))

    def test_12_package_plan(self):
        plan = load(X1 / "package-plan.json")
        self.assertEqual(len(plan["direct_additions"]), 3)
        self.assertEqual(plan["installed_in_x1"], 0)
        for row in plan["direct_additions"]:
            self.assertRegex(row["sha256"], r"^[0-9a-f]{64}$")

    def test_13_identity_practices(self):
        identity = load(X1 / "identity-and-practices.json")
        self.assertEqual(identity["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(len(identity["practices"]), 4)
        self.assertTrue(identity["successor_recommendation"])

    def test_14_sources_are_not_observations(self):
        ledger = load(X1 / "official-primary-source-ledger.json")
        self.assertGreaterEqual(len(ledger["entries"]), 10)
        self.assertEqual(ledger["real_rows"], 0)
        self.assertEqual(ledger["authority_actions"], 0)
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in ledger["entries"]))

    def test_15_route_held_and_future_identity_open(self):
        route = load(X1 / "route-plan.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["successor_contacted"])
        self.assertEqual(route["future_seat"], 8)
        self.assertFalse(route["future_seat_identity_preassigned"])

    def test_16_activation_count_layers(self):
        counts = load(X1 / "activation-count-overlay.json")
        self.assertEqual(counts["iveren_repository"]["effective_negatives"], 76876)
        self.assertEqual(counts["iveren_postcanonical_route_delta"]["effective_negatives"], 1)
        self.assertTrue(counts["source_induction_extra_failure_unaggregated"])
        self.assertEqual(counts["x1_current"]["effective_negatives"], 76884)

    def test_17_startup_negatives_nonerased(self):
        negatives = load(X1 / "startup-retained-negatives.json")
        self.assertEqual(len(negatives["records"]), 7)
        self.assertTrue(all(row["credit"] == 0 for row in negatives["records"]))

    def test_18_method_flow_outputs(self):
        ledger = load(BASE / "method-flow" / "ledger.json")
        self.assertEqual(len(ledger["methods"]), 7)
        self.assertEqual(len(ledger["witnesses"]), 14)
        self.assertEqual(sum(w["result"] == "fail" for w in ledger["witnesses"]), 7)
        self.assertEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 7)
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))

    def test_19_workflow_refinement(self):
        validation = load(BASE / "workflow-refinement" / "workflow-plan-validation.json")
        self.assertTrue(validation["valid"])

    def test_20_reflection_and_index(self):
        self.assertTrue(any((BASE / "reflection-remaster").glob("*.json")))
        self.assertTrue((BASE / "tooling" / "ghc-family-index.json").exists())

    def test_21_privacy_scan(self):
        scan = load(VALIDATION / "x1-privacy-scan.json")
        self.assertEqual(len(scan["pattern_classes"]), 5)
        self.assertEqual(scan["confirmed_hit_count"], 0)

    def test_22_manifest_matches_working_bytes(self):
        manifest = load(VALIDATION / "x1-manifest.json")
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), entry["bytes_normalized_lf"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_23_all_phase_json_parses(self):
        paths = list(BASE.rglob("*.json"))
        self.assertGreater(len(paths), 20)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_24_owner_file_ceiling(self):
        files = [path for path in BASE.rglob("*") if path.is_file()]
        self.assertLess(len(files) + 2, 2000)

    def test_25_document_caps(self):
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_26_staged_review_shape(self):
        review = load(VALIDATION / "x1-staged-review.json")
        self.assertIn(review["state"], {"PREPARED_NOT_STAGED", "PASS"})

    def test_27_workflow_request_has_no_private_route(self):
        text = (X1 / "workflow-plan-request.json").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
        self.assertIn("future-sibling-08-self-chosen", text)

    def test_28_threat_model(self):
        model = load(X1 / "threat-model.json")
        self.assertGreaterEqual(len(model["threats"]), 10)
        self.assertIn("canonical replay", model["threats"])

    def test_29_validation_scope(self):
        contract = load(X1 / "validation-contract.json")
        self.assertEqual(contract["execution_authority"], "owner_self_scoped_delta")
        self.assertFalse(contract["full_repository_suite"])
        self.assertEqual(contract["canonical_invocation_budget"], 1)
        self.assertFalse(contract["replay_after_success"])

    def test_30_terminal_verdict(self):
        self.assertEqual(load(X1 / "phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
