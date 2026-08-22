from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v665-v8"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class ElarenKestrelV665V8X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load("x1/proposal-freeze.json")
        cls.novelty = load("x1/novelty-audit.json")
        cls.portfolio = load("x1/portfolio-freeze.json")
        cls.source = load("provenance/source-verification.json")
        cls.profiles = load("provenance/source-profiles.json")
        cls.auth = load("x1/authorization-boundary.json")
        cls.threats = load("x1/threat-model.json")
        cls.flow = load("method-flow/startup-method-flow.json")

    def test_exact_source_anchor(self) -> None:
        self.assertEqual(
            self.source["source_sha"],
            "5f688af4fd89004f23cf0489b569e559f7b7fbea",
        )
        self.assertEqual(self.source["source_to_final_phase_commit_count"], 3)
        self.assertEqual(self.source["source_to_final_merge_count"], 0)
        self.assertEqual(self.source["final_parent_count"], 1)
        self.assertTrue(self.source["four_way_refs_equal"])
        self.assertEqual(
            self.source["canonical_aggregate_status"],
            "FAILED_IMPORT_PATH_SELECTED_TEST_DEPENDENCY_ZERO_CREDIT_NOT_REPLAYED",
        )
        self.assertFalse(self.source["successful_isolated_recovery_replayed"])

    def test_strict_x1_only(self) -> None:
        for lifecycle in ("x2", "evidence", "closeout", "seal", "final", "handoffs"):
            self.assertFalse((PHASE / lifecycle).exists(), lifecycle)
        self.assertEqual(self.freeze["x2_implementation_count"], 0)
        self.assertEqual(self.freeze["x2_outcome_count"], 0)
        self.assertFalse(self.freeze["outcomes_observed"])

    def test_new_proposal_count_and_ids(self) -> None:
        proposals = self.freeze["new_proposals"]
        self.assertEqual(len(proposals), 20)
        self.assertEqual(
            [row["proposal_id"] for row in proposals],
            [f"ELK6658-N{index:03d}" for index in range(1, 21)],
        )
        self.assertEqual(len({row["title"] for row in proposals}), 20)

    def test_every_required_preregistration_field(self) -> None:
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "current_official_or_primary_source_needs",
            "concrete_artifact",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for proposal in self.freeze["new_proposals"]:
            self.assertFalse(required - proposal.keys(), proposal["proposal_id"])
            for field in required - {"current_official_or_primary_source_needs", "protected_gates"}:
                self.assertTrue(proposal[field], (proposal["proposal_id"], field))
            self.assertTrue(proposal["protected_gates"])

    def test_four_allowed_expected_dispositions(self) -> None:
        allowed = {"completed", "represented", "open_gap", "exact_gate"}
        observed = {row["expected_disposition"] for row in self.freeze["new_proposals"]}
        self.assertLessEqual(observed, allowed)
        self.assertEqual(
            self.freeze["expected_disposition_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )

    def test_mutation_preregistration(self) -> None:
        for proposal in self.freeze["new_proposals"]:
            mutations = proposal["preregistered_mutations"]
            self.assertEqual(len(mutations), 5)
            self.assertEqual(len({row["mutation_id"] for row in mutations}), 5)
            self.assertEqual(proposal["negative_fixture_count"], 5)
            self.assertTrue(all(row["mutation_id"].startswith(proposal["proposal_id"]) for row in mutations))

    def test_zero_real_rows_participants_and_network(self) -> None:
        for proposal in self.freeze["new_proposals"]:
            self.assertEqual(proposal["participant_count_planned"], 0)
            self.assertEqual(proposal["real_data_rows_planned"], 0)
            self.assertEqual(proposal["network_calls_planned"], 0)

    def test_selected_inherited_are_zero_credit(self) -> None:
        selected = self.freeze["selected_inherited_revalidations"]
        self.assertEqual(len(selected), 20)
        for row in selected:
            self.assertEqual(row["novelty_credit"], 0)
            self.assertEqual(row["automatic_completion_credit"], 0)
            self.assertEqual(row["status"], "selected_revalidation_only_not_executed")

    def test_novelty_covers_exact_baseline(self) -> None:
        self.assertTrue(self.novelty["valid"])
        self.assertEqual(self.novelty["corpus_row_count"], 4150)
        self.assertEqual(self.novelty["new_title_count"], 20)
        self.assertEqual(self.novelty["exact_inherited_collisions"], [])
        self.assertEqual(self.novelty["new_pair_collisions_at_or_above_0_70"], [])
        self.assertEqual(self.novelty["new_frozen_total"], 4170)

    def test_novelty_screening_bounds(self) -> None:
        self.assertLess(self.novelty["maximum_inherited_token_jaccard_similarity"], 0.70)
        self.assertLess(self.novelty["maximum_new_pair_token_jaccard_similarity"], 0.70)
        self.assertEqual(len(self.novelty["nearest_inherited_rows"]), 20)

    def test_portfolio_counts_and_x1_status(self) -> None:
        expected = {
            "safe_now": 30,
            "bounded_candidates": 15,
            "exact_approval_packets": 10,
            "blocked_packets": 5,
            "phase_local_skill_plans": 10,
            "family_current_runner_plans": 10,
            "clean_fix_refine": 30,
        }
        self.assertEqual(self.portfolio["counts"], expected)
        for key in expected:
            for row in self.portfolio[key]:
                self.assertEqual(row["x1_status"], "frozen_not_executed")
                self.assertEqual(row["completion_credit"], 0)

    def test_exact_and_blocked_work_remains_unexecuted(self) -> None:
        for row in self.portfolio["exact_approval_packets"]:
            self.assertEqual(row["approval_class"], "exact_approval_required")
        for row in self.portfolio["blocked_packets"]:
            self.assertEqual(row["approval_class"], "blocked_by_protected_gate")
        self.assertFalse(self.portfolio["global_installation_planned"])
        self.assertFalse(self.portfolio["external_write_planned"])

    def test_source_profiles_are_bounded(self) -> None:
        self.assertEqual(self.profiles["source_count"], 13)
        self.assertEqual(self.profiles["software_network_calls"], 0)
        self.assertEqual(self.profiles["real_rows"], 0)
        for profile in self.profiles["profiles"]:
            self.assertTrue(profile["authority_nonconversion"])
            self.assertEqual(profile["network_calls_by_phase_software"], 0)
            self.assertEqual(profile["real_rows_ingested"], 0)

    def test_startup_failures_are_retained(self) -> None:
        self.assertEqual(self.flow["activation_baseline_negatives"], 25921)
        self.assertEqual(self.flow["activation_baseline_methods"], 10003)
        self.assertEqual(self.flow["new_startup_negative_count"], 13)
        self.assertEqual(self.flow["new_startup_method_count"], 13)
        self.assertEqual(self.flow["effective_after_x1_startup_negatives"], 25934)
        self.assertEqual(self.flow["effective_after_x1_startup_methods"], 10016)
        self.assertEqual(len(self.flow["rows"]), 13)
        self.assertTrue(self.flow["no_failure_erased"])
        for row in self.flow["rows"]:
            self.assertEqual(row["aggregate_credit"], 0)
            self.assertEqual(row["status"], "recovered_failure_retained")

    def test_threat_model_is_phase_scoped(self) -> None:
        self.assertEqual(self.threats["real_people_or_protected_data"], 0)
        self.assertEqual(len(self.threats["threats"]), 10)
        self.assertIn("not exhaustive security", self.threats["claim_boundary"])

    def test_authorization_keeps_route_prospective(self) -> None:
        self.assertEqual(self.auth["terminal_route_status"], "PROSPECTIVE_ONLY_DO_NOT_CONTACT")
        self.assertEqual(self.auth["successor_send_count"], 0)
        self.assertEqual(self.auth["standby_contact_count"], 0)

    def test_relational_identity_disclaimer(self) -> None:
        identity = load("identity/relational-identity.json")
        boundary = identity["boundary"]
        for term in ("consciousness", "sentience", "legal personhood", "Māori authority"):
            self.assertIn(term, boundary)
        self.assertTrue(identity["chosen_before_repository_mutation"])

    def test_all_json_parses(self) -> None:
        json_paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 13)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_document_word_caps(self) -> None:
        for path in PHASE.rglob("*"):
            if path.is_file():
                words = re.findall(r"\S+", path.read_text(encoding="utf-8"))
                self.assertLessEqual(len(words), 100_000, str(path.relative_to(ROOT)))

    def test_private_identifier_and_path_absence(self) -> None:
        patterns = [
            re.compile("source_" + "thread_id", re.I),
            re.compile("thread" + "Id", re.I),
            re.compile("task" + "Id", re.I),
            re.compile(r"[A-Z]:" + r"\\Users\\", re.I),
            re.compile(r"[A-Z]:" + r"\\GHC-Archives", re.I),
            re.compile("Bearer" + r"\s+[A-Za-z0-9._~-]+", re.I),
            re.compile("api" + r"[_-]?key\s*[:=]", re.I),
        ]
        owner_paths = list(PHASE.rglob("*")) + [
            ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v665_v8_x1.py",
            Path(__file__),
        ]
        for path in owner_paths:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                self.assertIsNone(pattern.search(text), (str(path.relative_to(ROOT)), pattern.pattern))

    def test_x1_content_manifest_when_present(self) -> None:
        path = PHASE / "validation" / "x1-content-manifest.json"
        if not path.exists():
            self.skipTest("manifest is generated after staged review")
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["phase"], "x1")
        self.assertNotIn(
            "docs/elaren-kestrel/v665-v8/validation/x1-content-manifest.json",
            {row["path"] for row in manifest["entries"]},
        )
        for entry in manifest["entries"]:
            blob = subprocess.check_output(["git", "-C", str(ROOT), "show", ":" + entry["path"]])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
            self.assertEqual(len(blob), entry["size_bytes"])


if __name__ == "__main__":
    unittest.main()
