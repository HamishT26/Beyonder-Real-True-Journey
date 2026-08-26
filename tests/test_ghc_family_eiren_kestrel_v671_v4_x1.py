"""Owner-scoped tests for Eiren Kestrel v671-v4 planning-only x1."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v671-v4"
SOURCE = "37ac80c499d43a90c874876402b262a220a252a1"
BRANCH = "codex/GHC-Family/eiren-kestrel-v671-v4-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=False, timeout=60
    )
    if result.returncode:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


class EirenKestrelV671V4X1Tests(unittest.TestCase):
    def test_01_exact_branch_and_source_head(self):
        self.assertEqual(git("symbolic-ref", "--short", "HEAD").decode().strip(), BRANCH)
        self.assertEqual(git("rev-parse", "HEAD").decode().strip(), SOURCE)

    def test_02_activation_and_source_receipt_were_verified_without_replay(self):
        source = load("x1/activation-intake.json")["source_verification"]
        self.assertTrue(all(source["checks"].values()))
        self.assertEqual(source["source_manifests_replayed"], 0)
        self.assertFalse(source["source_canonical_replayed"])
        self.assertEqual(source["canonical_receipt"]["invocation_count"], 1)
        self.assertFalse(source["canonical_receipt"]["replayed"])

    def test_03_source_parent_chain_and_history_are_exact(self):
        source = load("x1/activation-intake.json")["source_verification"]
        self.assertEqual(source["phase_commits"], 3)
        self.assertEqual(source["merge_commits"], 0)
        self.assertEqual(
            source["parent_chain"],
            {
                "x1_parent": "33b7c2d6b9f79f931ff98c478f136dab823c4d69",
                "evidence_parent": "2551c126776ea0538354a32b90414f31f5cec4b3",
                "final_parent": "46c41e84871edd72544ddad16f038902ec2386f5",
            },
        )

    def test_04_identity_is_relational_and_corrigible(self):
        row = load("x1/identity-and-boundary.json")
        text = row["identity_boundary"].lower()
        for phrase in (
            "relational working language only",
            "not evidence of consciousness",
            "identity continuity",
            "independent agency",
            "maori authority",
        ):
            self.assertIn(phrase, text)
        self.assertIn("rename", row["corrigibility"])
        self.assertIn("stop", row["corrigibility"])

    def test_05_exactly_forty_unique_proposals_with_required_fields(self):
        rows = load("x1/proposals.json")["rows"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        self.assertEqual(len({row["title"] for row in rows}), 40)
        required = {
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
        for row in rows:
            self.assertTrue(required <= set(row))
            self.assertEqual(set(row["protected_gates"]) >= {"empirical", "professional", "legal", "cultural", "Maori_authority", "Stage_20"}, True)
            self.assertEqual(row["x1_state"], "frozen_not_executed")
            self.assertEqual(row["real_people"], 0)
            self.assertEqual(row["real_records_or_objects"], 0)
            self.assertEqual(row["external_actions"], 0)

    def test_06_expected_outcomes_use_only_four_labels(self):
        proposal = load("x1/proposals.json")
        self.assertEqual(proposal["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        observed = {label: 0 for label in LABELS}
        for row in proposal["rows"]:
            self.assertIn(row["expected_disposition"], LABELS)
            observed[row["expected_disposition"]] += 1
        self.assertEqual(observed, proposal["outcomes"])

    def test_07_semantic_audit_is_bounded_and_collision_free(self):
        audit = load("x1/semantic-neighbor-audit.json")
        self.assertEqual(audit["declared_source_chain"], 5670)
        self.assertEqual(audit["new_titles"], 40)
        self.assertEqual(audit["collisions"], 0)
        self.assertLess(audit["max_jaccard"], audit["collision_threshold"])
        self.assertFalse(audit["universal_novelty_claim"])
        self.assertTrue(audit["canonical_row_mapping_open_gap"])
        self.assertGreaterEqual(audit["audited_unique_titles"], 5617)
        self.assertGreaterEqual(audit["accessible_ref_corpus"]["unique_proposal_ids"], 6220)
        self.assertGreaterEqual(audit["accessible_ref_corpus"]["semantic_occurrences"], 262244)
        self.assertIn("reachable through local and remote refs", audit["accessible_ref_corpus"]["scope"])
        self.assertEqual(len(audit["rows"]), 40)

    def test_08_primary_and_protected_pillars_are_visible(self):
        truth = load("x1/phase-truth.json")
        self.assertEqual(truth["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(set(truth["protected_pillars"]), {"GMUT Mind", "THOS Body"})
        self.assertIn("seed-library", truth["bounded_human_practice"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_09_x1_is_planning_only(self):
        truth = load("x1/phase-truth.json")
        self.assertEqual(truth["x1_completion_credit"], 0)
        self.assertFalse(truth["x2_execution_started"])
        self.assertEqual(truth["real_world_actions"], 0)
        self.assertEqual(truth["external_writes"], 0)
        self.assertFalse((OWNER_ROOT / "x2").exists())

    def test_10_startup_failures_and_recoveries_are_retained(self):
        flow = load("x1/method-flow-startup.json")
        self.assertEqual(flow["row_count"], 8)
        self.assertTrue(flow["all_failures_retained"])
        self.assertTrue(flow["all_recoveries_paired"])
        self.assertTrue(all(row["fail_witness"]["credit"] == 0 for row in flow["rows"]))
        self.assertTrue(all(row["pass_witness"]["state"] == "bounded_pass" for row in flow["rows"]))
        self.assertEqual(flow["counts"]["effective_negatives"], 33913)
        self.assertEqual(flow["counts"]["effective_methods"], 20230)

    def test_11_repository_seal_and_external_overlay_remain_separate(self):
        row = load("x1/source-count-overlay.json")
        self.assertEqual(row["repository_sealed"]["effective_negatives"], 33905)
        self.assertEqual(row["activation_external_overlay"]["effective_negatives"], 33905)
        self.assertFalse(row["repository_seal_rewritten"])
        validation = load("x1/validation-negative-overlay.json")
        self.assertEqual(validation["row_count"], 1)
        self.assertEqual(validation["effective_counts"]["effective_negatives"], 33914)
        self.assertTrue(validation["all_failures_retained"])

    def test_12_portfolio_is_frozen_without_execution_credit(self):
        row = load("x1/portfolio-freeze.json")
        self.assertEqual(row["counts"]["safe_now"], 60)
        self.assertEqual(row["counts"]["candidates"], 30)
        self.assertEqual(row["counts"]["exact_approval"], 20)
        self.assertEqual(row["counts"]["blocked"], 10)
        self.assertEqual(row["counts"]["skills"], 20)
        self.assertEqual(row["counts"]["runners"], 10)
        self.assertEqual(row["counts"]["clean_fix_refine"], 60)
        self.assertTrue(row["filler_prohibited"])
        self.assertEqual(row["inherited_portfolio_completion_credit"], 0)

    def test_13_sources_are_official_vocabulary_only_and_zero_row(self):
        row = load("x1/source-ledger.json")
        self.assertEqual(len(row["sources"]), 6)
        self.assertEqual(row["adapter_calls"], 0)
        self.assertEqual(row["downloads"], 0)
        self.assertEqual(row["real_rows"], 0)
        self.assertEqual(row["external_writes"], 0)
        self.assertIn("not observations", row["boundary"])

    def test_14_threat_model_preserves_required_risks(self):
        row = load("x1/threat-model.json")
        risks = " ".join(item["risk"] for item in row["risks"]).lower()
        for phrase in ("novelty", "seed-library", "failure", "private", "accessibility", "duplicate"):
            self.assertIn(phrase, risks)
        self.assertTrue(row["not_exhaustive_security"])

    def test_15_route_is_unresolved_and_nobody_was_contacted(self):
        row = load("x1/route-plan.json")
        self.assertIsNone(row["prospective_recipient_exact_title"])
        self.assertIsNone(row["prospective_phase"])
        self.assertEqual(row["delivery_state"], "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH")
        self.assertEqual(row["successor_contact_count"], 0)
        self.assertEqual(row["task_creation_count"], 0)
        self.assertEqual(row["standby_contact_count"], 0)

    def test_16_all_owner_json_parses(self):
        paths = sorted(OWNER_ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 10)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_17_x1_staged_review_and_privacy_are_valid(self):
        review = load("validation/x1-staged-review.json")
        privacy = load("validation/x1-staged-privacy.json")
        receipt = load("validation/x1-validation-receipt.json")
        self.assertTrue(review["valid"])
        self.assertTrue(review["planning_only"])
        self.assertEqual(review["deleted_paths"], [])
        self.assertEqual(review["x2_paths"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["source_canonical_replayed"])
        self.assertEqual(receipt["source_manifests_replayed"], 0)

    def test_18_x1_manifest_matches_exact_staged_blobs(self):
        manifest = load("validation/x1-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_staged_git_blob")
        for entry in manifest["entries"]:
            blob = git("show", f":{entry['path']}").replace(b"\r\n", b"\n")
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])


if __name__ == "__main__":
    unittest.main()
