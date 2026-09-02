from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-ash" / "v684-v6"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"


def load(name: str):
    return json.loads((X1 / name).read_text(encoding="utf-8"))


class CaelenAshV684V6X1Tests(unittest.TestCase):
    def test_01_phase_is_planning_only(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["lifecycle"], "X1_PLANNING_ONLY_PRECOMMIT")
        self.assertFalse(truth["x2_paths_created"])
        self.assertEqual(truth["executed_outcomes"], 0)
        self.assertFalse((BASE / "x2").exists())
        self.assertFalse((BASE / "final").exists())

    def test_02_source_anchors(self):
        source = load("source-verification.json")
        self.assertEqual(source["source_head"], "9a2fcdc6021dcc8226ff7150b990bfe429671680")
        self.assertEqual(source["verified_before_mutation"]["phase_commits"], 4)
        self.assertEqual(source["verified_before_mutation"]["merge_commits"], 0)
        self.assertTrue(source["verified_before_mutation"]["local_upstream_tracking_fresh_live_equal"])
        self.assertEqual(source["verified_before_mutation"]["manifest_entries_replayed"], 595)

    def test_03_exact_sixty_new_proposals(self):
        freeze = load("new-proposal-freeze.json")
        self.assertTrue(freeze["planning_only"])
        self.assertEqual(len(freeze["entries"]), 60)
        self.assertEqual(len({entry["proposal_id"] for entry in freeze["entries"]}), 60)
        self.assertEqual(len({entry["title"] for entry in freeze["entries"]}), 60)
        self.assertEqual(freeze["mutation_count"], 300)

    def test_04_proposal_required_fields(self):
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "current_official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for entry in load("new-proposal-freeze.json")["entries"]:
            self.assertTrue(required.issubset(entry))
            self.assertEqual(len(entry["preregistered_rejecting_mutations"]), 5)
            self.assertTrue(entry["planning_only"])

    def test_05_expected_label_counts(self):
        freeze = load("new-proposal-freeze.json")
        self.assertEqual(
            freeze["expected_counts"],
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )
        self.assertEqual(
            set(freeze["allowed_outcomes"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )

    def test_06_inherited_credit_is_zero(self):
        inherited = load("inherited-revalidation-freeze.json")
        self.assertEqual(inherited["count"], 60)
        self.assertTrue(all(item["caelen_novelty_credit"] == 0 for item in inherited["entries"]))
        self.assertTrue(all(item["caelen_completion_credit"] == 0 for item in inherited["entries"]))

    def test_07_chain_audit(self):
        audit = load("proposal-chain-audit.json")
        self.assertEqual(audit["declared_chain_before"], 10970)
        self.assertEqual(audit["declared_chain_after_x1_freeze"], 11030)
        self.assertEqual(audit["exact_collision_with_immediate_sable_titles"], [])
        self.assertEqual(audit["retained_artifact_title_probe"]["exact_new_title_collisions"], [])
        self.assertFalse(audit["universal_novelty_claim"])

    def test_08_portfolio_counts(self):
        portfolio = load("portfolio-freeze.json")
        self.assertEqual(len(portfolio["safe_now"]), 120)
        self.assertEqual(len(portfolio["owner_candidates"]), 80)
        self.assertTrue(portfolio["caps_are_ceilings"])
        cfr = load("clean-fix-refine-plan.json")
        self.assertEqual(len(cfr["entries"]), 100)
        self.assertTrue(all(not item["destructive"] for item in cfr["entries"]))

    def test_09_holds_are_visible_and_unexecuted(self):
        holds = load("approval-hold-register.json")
        self.assertEqual(len(holds["exact_approval_packets"]), 20)
        self.assertEqual(len(holds["blocked_packets"]), 10)
        self.assertTrue(all(item["state"] == "HELD_UNEXECUTED" for item in holds["exact_approval_packets"]))
        self.assertTrue(all(item["state"] == "BLOCKED_UNEXECUTED" for item in holds["blocked_packets"]))

    def test_10_skill_and_runner_plans(self):
        plan = load("skill-runner-plan.json")
        self.assertEqual(len(plan["skills"]), 20)
        self.assertEqual(len(plan["runners"]), 10)
        self.assertTrue(all(item["state"] == "PLANNED_NOT_BUILT" for item in plan["skills"]))
        self.assertTrue(all(item["state"] == "PLANNED_NOT_BUILT" for item in plan["runners"]))
        self.assertFalse(plan["global_installation"])

    def test_11_sources_are_context_not_observation(self):
        ledger = load("official-primary-source-ledger.json")
        self.assertGreaterEqual(len(ledger["entries"]), 8)
        self.assertEqual(ledger["real_rows"], 0)
        self.assertEqual(ledger["network_downloads_of_domain_data"], 0)
        self.assertEqual(ledger["authority_actions"], 0)

    def test_12_method_flow_nonerasure(self):
        method = load("method-flow-startup.json")
        self.assertEqual(len(method["startup_failures"]), 16)
        self.assertEqual(len(method["recovery_methods"]), 12)
        self.assertEqual(method["derived_after_startup"]["effective_negatives"], 59428)
        self.assertEqual(method["derived_after_startup"]["effective_methods"], 73688)
        self.assertEqual(method["derived_after_startup"]["failed_witnesses"], 30789)
        self.assertEqual(method["derived_after_startup"]["bounded_passing_witnesses"], 54223)

    def test_13_privacy_scan_zero_confirmed(self):
        scan = json.loads((VALIDATION / "x1-privacy-scan.json").read_text(encoding="utf-8"))
        self.assertEqual(len(scan["pattern_classes"]), 5)
        self.assertEqual(scan["confirmed_hit_count"], 0)
        self.assertEqual(scan["confirmed_hits"], [])

    def test_14_manifest_matches_working_files(self):
        manifest = json.loads((VALIDATION / "x1-index-manifest.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(manifest["entry_count"], 20)
        self.assertEqual(len(manifest["self_exclusions"]), 3)
        for entry in manifest["entries"]:
            path = ROOT / entry["path"]
            data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_15_all_json_parses(self):
        json_paths = sorted(BASE.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 20)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_16_route_held(self):
        route = load("route-plan.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["next_title_if_fresh_terminal_authority_still_matches"], "Orin Thale")

    def test_17_exact_branch_and_base(self):
        branch = subprocess.run(
            ["git", "branch", "--show-current"], cwd=ROOT, check=True, text=True, capture_output=True
        ).stdout.strip()
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
        ).stdout.strip()
        self.assertEqual(branch, "codex/GHC-Family/caelen-ash-v684-v6-full-tools")
        self.assertEqual(head, "9a2fcdc6021dcc8226ff7150b990bfe429671680")

    def test_18_document_caps(self):
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_19_owner_file_ceiling(self):
        self.assertLess(len([path for path in BASE.rglob("*") if path.is_file()]), 2000)

    def test_20_staged_review_shape(self):
        review = json.loads((VALIDATION / "x1-staged-review.json").read_text(encoding="utf-8"))
        self.assertIn(review["state"], {"PREPARED_NOT_STAGED", "PASS"})
        if review["state"] == "PASS":
            self.assertEqual(review["manifest_mismatches"], [])
            self.assertEqual(review["missing_paths"], [])
            self.assertEqual(review["out_of_scope_paths"], [])
            self.assertTrue(review["x1_only"])


if __name__ == "__main__":
    unittest.main()
