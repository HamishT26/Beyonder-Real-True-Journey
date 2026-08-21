"""Owner-scoped tests for Orin Thale v665-v1's bounded x2 evidence."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v665-v1"
X1_HEAD = "1e9a49b0cc377ba2eafd90fb09e478c88f8f1f3b"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def strict_json(path: Path):
    def reject_duplicates(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate key {key} in {path}")
            value[key] = item
        return value

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


class OrinV665V1X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = strict_json(PHASE / "x1/proposal-freeze.json")
        cls.boundary = strict_json(PHASE / "x2/x1-boundary-receipt.json")
        cls.outcomes = strict_json(PHASE / "x2/outcome-ledger.json")
        cls.mutations = strict_json(PHASE / "x2/mutation-summary.json")
        cls.inherited = strict_json(PHASE / "x2/inherited-contract-integrity.json")
        cls.skills = strict_json(PHASE / "x2/skill-build-receipt.json")
        cls.runners = strict_json(PHASE / "x2/runner-invocation-receipt.json")
        cls.portfolio = strict_json(PHASE / "x2/portfolio-execution.json")
        cls.methods = strict_json(PHASE / "x2/method-flow-state.json")
        cls.negatives = strict_json(PHASE / "x2/retained-negative-register.json")
        cls.gates = strict_json(PHASE / "x2/exact-open-gate-register.json")
        cls.sources = strict_json(PHASE / "x2/source-status-review.json")
        cls.environment = strict_json(PHASE / "x2/environment-version-receipt.json")
        cls.threats = strict_json(PHASE / "x2/threat-model-results.json")
        cls.wellbeing = strict_json(PHASE / "x2/wellbeing-check.json")
        cls.accessibility = strict_json(PHASE / "x2/accessibility-reservation.json")
        cls.reproduction = strict_json(PHASE / "x2/reproduction-receipt.json")
        cls.stage20 = strict_json(PHASE / "x2/stage20-evidence-board.json")

    def test_01_x1_boundary_is_exact(self) -> None:
        self.assertEqual(self.boundary["x1_head"], X1_HEAD)
        self.assertEqual(
            self.boundary["source_final"], "3ec44a944aabe16f64335383885c39d9592bf849"
        )
        self.assertTrue(self.boundary["direct_child"])
        self.assertTrue(self.boundary["clean_before_x2"])
        self.assertTrue(self.boundary["valid"])

    def test_02_x1_manifest_replayed(self) -> None:
        self.assertEqual(self.boundary["manifest_entry_count"], 12)
        self.assertEqual(self.boundary["manifest_exclusion_count"], 3)
        self.assertEqual(self.boundary["manifest_mismatch_count"], 0)
        self.assertFalse(self.boundary["x1_contains_observed_x2_outcomes"])

    def test_03_core_outcome_arithmetic(self) -> None:
        self.assertEqual(
            self.outcomes["counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(self.outcomes["proposal_count"], 20)
        self.assertEqual(self.outcomes["unknown_outcome_count"], 0)
        self.assertTrue(self.outcomes["valid"])

    def test_04_only_allowed_outcomes(self) -> None:
        self.assertEqual(set(self.outcomes["allowed_outcomes"]), ALLOWED)
        self.assertEqual({row["disposition"] for row in self.outcomes["outcomes"]}, ALLOWED)

    def test_05_all_twenty_surfaces_exist(self) -> None:
        rows = self.freeze["new_proposals"]
        self.assertEqual(len(rows), 20)
        for row in rows:
            slug = row["concrete_artifacts"][0].split("/")[2]
            for name in ("contract.json", "mutation-results.json", "bounded-receipt.json"):
                self.assertTrue((PHASE / "x2/surfaces" / slug / name).is_file())

    def test_06_positive_fixtures_are_bounded(self) -> None:
        for row in self.freeze["new_proposals"]:
            slug = row["concrete_artifacts"][0].split("/")[2]
            contract = strict_json(PHASE / "x2/surfaces" / slug / "contract.json")
            fixture = contract["positive_fixture"]
            self.assertTrue(contract["valid"])
            self.assertTrue(fixture["synthetic_only"])
            self.assertEqual(fixture["real_record_count"], 0)
            self.assertFalse(fixture["authority_claim"])
            self.assertFalse(fixture["empirical_claim"])
            self.assertFalse(fixture["production_claim"])
            self.assertEqual(fixture["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_07_five_mutations_per_proposal(self) -> None:
        for row in self.freeze["new_proposals"]:
            slug = row["concrete_artifacts"][0].split("/")[2]
            receipt = strict_json(PHASE / "x2/surfaces" / slug / "mutation-results.json")
            self.assertEqual(receipt["expected_count"], 5)
            self.assertEqual(len(receipt["results"]), 5)
            self.assertTrue(receipt["all_rejected"])
            self.assertEqual(receipt["failure_erasure_count"], 0)

    def test_08_all_hundred_mutations_retained(self) -> None:
        self.assertEqual(self.mutations["executed_mutation_count"], 100)
        self.assertEqual(self.mutations["rejected_mutation_count"], 100)
        self.assertEqual(self.mutations["accepted_mutation_count"], 0)
        self.assertEqual(self.mutations["retained_negative_count"], 100)
        self.assertEqual(self.mutations["failure_erasure_count"], 0)

    def test_09_surface_receipts_match_freeze(self) -> None:
        frozen = {row["proposal_id"]: row["expected_disposition"] for row in self.freeze["new_proposals"]}
        for row in self.outcomes["outcomes"]:
            self.assertEqual(row["disposition"], frozen[row["proposal_id"]])
            self.assertIn("bounded same-owner", row["scope"])

    def test_10_inherited_rows_are_zero_credit(self) -> None:
        self.assertEqual(self.inherited["row_count"], 20)
        self.assertEqual(self.inherited["novelty_credit"], 0)
        self.assertEqual(self.inherited["automatic_completion_credit"], 0)
        self.assertEqual(self.inherited["orin_new_outcome_credit"], 0)
        self.assertTrue(all(row["valid"] for row in self.inherited["results"]))

    def test_11_ten_skills_customized_and_validated(self) -> None:
        self.assertEqual(self.skills["skill_count"], 10)
        self.assertEqual(self.skills["customized_count"], 10)
        self.assertEqual(self.skills["quick_validated_count"], 10)
        self.assertEqual(self.skills["smoke_used_count"], 10)
        self.assertEqual(self.skills["global_install_count"], 0)
        self.assertTrue(self.skills["valid"])

    def test_12_skill_preflight_guards_prevented_repeat_failures(self) -> None:
        guards = self.skills["preflight_recurrence_guards"]
        self.assertTrue(guards["exact_directory_argument"])
        self.assertTrue(guards["process_local_utf8"])
        self.assertTrue(guards["unicode_authority_wording_preserved"])
        self.assertEqual(guards["new_validator_failure_count"], 0)

    def test_13_skill_files_have_required_boundaries(self) -> None:
        for row in self.skills["skills"]:
            path = ROOT / row["phase_local_path"]
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname: ghc-family-"))
            self.assertIn("## Workflow", text)
            self.assertIn("## Boundaries", text)
            self.assertIn("Māori concepts remain under Māori authority", text)

    def test_14_ten_family_runners_smoke_used(self) -> None:
        self.assertEqual(self.runners["runner_count"], 10)
        self.assertEqual(self.runners["family_compatible_count"], 10)
        self.assertEqual(self.runners["smoke_used_count"], 10)
        self.assertEqual(self.runners["real_record_count"], 0)
        self.assertEqual(self.runners["real_object_or_material_count"], 0)
        self.assertEqual(self.runners["empirical_row_count"], 0)
        self.assertEqual(self.runners["participant_or_operator_observation_count"], 0)
        self.assertTrue(self.runners["valid"])

    def test_15_each_runner_is_callable(self) -> None:
        for _, runner, _ in [
            ("a", "ghc_family_variational_bicomplex_boundary.py", ""),
            ("b", "ghc_family_jet_atlas_quarantine.py", ""),
            ("c", "ghc_family_contact_degree_guard.py", ""),
            ("d", "ghc_family_euler_boundary_lineage.py", ""),
            ("e", "ghc_family_millinery_topology_vacancy.py", ""),
            ("f", "ghc_family_millinery_material_state.py", ""),
            ("g", "ghc_family_thos_bench_handover.py", ""),
            ("h", "ghc_family_freed_id_work_envelope.py", ""),
            ("i", "ghc_family_millinery_rights_authority.py", ""),
            ("j", "ghc_family_stage20_model_nonpromotion.py", ""),
        ]:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / runner), "--json"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(result.returncode, 0, runner)
            self.assertTrue(json.loads(result.stdout)["valid"])

    def test_16_owner_portfolio_execution_counts(self) -> None:
        self.assertEqual(
            self.portfolio["counts"],
            {
                "owner_safe_now_executed": 30,
                "owner_candidates_executed": 15,
                "owner_skill_tasks_executed": 10,
                "owner_runner_tasks_executed": 10,
                "owner_clean_fix_refine_executed": 30,
                "exact_approval_executed": 0,
                "blocked_executed": 0,
                "successor_recommendation_executed": 0,
            },
        )
        self.assertTrue(self.portfolio["valid"])

    def test_17_exact_and_blocked_remain_unexecuted(self) -> None:
        rows = self.portfolio["exact_approval_packets"] + self.portfolio["blocked_packets"]
        self.assertEqual(len(rows), 15)
        self.assertFalse(any(row["executed"] for row in rows))
        self.assertTrue(all(row["current_owner_completion_credit"] == 0 for row in rows))

    def test_18_successor_recommendations_remain_zero_credit(self) -> None:
        rows = [
            row
            for group in self.portfolio["successor_recommendations"].values()
            for row in group
        ]
        self.assertEqual(len(rows), 85)
        self.assertFalse(any(row["executed"] for row in rows))
        self.assertTrue(all(row["orin_completion_credit"] == 0 for row in rows))

    def test_19_retained_negative_arithmetic(self) -> None:
        self.assertEqual(self.negatives["caelen_repository_sealed_negatives"], 25_071)
        self.assertFalse(self.negatives["caelen_repository_count_rewritten"])
        self.assertEqual(self.negatives["user_delivered_activation_negatives"], 25_073)
        self.assertEqual(self.negatives["inherited_post_send_external_negatives"], 0)
        self.assertEqual(self.negatives["orin_startup_negatives"], 9)
        self.assertEqual(self.negatives["x2_tool_contract_negatives"], 2)
        self.assertEqual(self.negatives["executed_rejecting_mutation_negatives"], 100)
        self.assertEqual(self.negatives["effective_negatives"], 25_184)
        self.assertEqual(self.negatives["failed_witness_erasure_count"], 0)

    def test_20_method_flow_arithmetic(self) -> None:
        self.assertEqual(self.methods["x2_new_retained_negative_count"], 102)
        self.assertEqual(self.methods["x2_new_method_count"], 32)
        self.assertEqual(len(self.methods["methods"]), 32)
        self.assertEqual(self.methods["effective_negatives"], 25_184)
        self.assertEqual(self.methods["effective_methods"], 9_046)
        self.assertEqual(self.methods["failure_erasure_count"], 0)

    def test_21_each_method_has_failed_and_passing_witnesses(self) -> None:
        for row in self.methods["methods"]:
            self.assertEqual(row["state"], "preferred")
            self.assertEqual(row["failed_witness_credit"], "zero")
            self.assertTrue(row["failed_witness"])
            self.assertTrue(row["passing_witness"])

    def test_22_open_and_exact_gate_arithmetic(self) -> None:
        self.assertEqual(self.gates["inherited_open_gaps"], 174)
        self.assertEqual(self.gates["new_open_gaps"], 1)
        self.assertEqual(self.gates["effective_open_gaps"], 175)
        self.assertEqual(self.gates["inherited_exact_gates"], 172)
        self.assertEqual(self.gates["new_exact_gates"], 1)
        self.assertEqual(self.gates["effective_exact_gates"], 173)
        self.assertEqual(self.gates["gate_erasure_count"], 0)

    def test_23_sources_are_version_only(self) -> None:
        self.assertEqual(self.sources["reviewed_source_count"], 11)
        self.assertEqual(self.sources["official_or_primary_count"], 11)
        self.assertEqual(self.sources["live_data_calls"], 0)
        self.assertEqual(self.sources["empirical_row_downloads"], 0)
        self.assertTrue(self.sources["version_verification_only"])

    def test_24_gmut_remains_symbolic(self) -> None:
        row = strict_json(PHASE / "x2/pillars/gmut-model-family.json")
        self.assertEqual(row["real_observations"], 0)
        self.assertEqual(row["likelihood_evaluations"], 0)
        self.assertEqual(row["parameter_constraints"], 0)
        self.assertIn("theory_of_everything", row["claims_refused"])
        self.assertEqual(row["disposition"], "represented")

    def test_25_thos_remains_proxy(self) -> None:
        row = strict_json(PHASE / "x2/pillars/thos-proxy.json")
        self.assertEqual(row["participants"], 0)
        self.assertEqual(row["operators"], 0)
        self.assertFalse(row["safety_monitoring"])
        self.assertFalse(row["statistics"])
        self.assertFalse(row["independent_review"])
        self.assertFalse(row["operational_effectiveness_claim"])

    def test_26_freed_id_remains_nonproduction(self) -> None:
        row = strict_json(PHASE / "x2/pillars/freed-id-nonproduction.json")
        self.assertEqual(row["real_keys"], 0)
        self.assertEqual(row["real_proofs"], 0)
        self.assertFalse(row["production_ready"])
        self.assertFalse(row["trust_governance"])

    def test_27_cbr_authority_is_exact_gated(self) -> None:
        row = strict_json(PHASE / "x2/pillars/cbr-authority-matrix.json")
        self.assertEqual(row["authority_decisions"], 0)
        self.assertEqual(row["affected_party_acceptances"], 0)
        self.assertEqual(row["maori_authority_decisions"], 0)
        self.assertEqual(row["disposition"], "exact_gate")
        self.assertIn("Māori concepts remain under Māori authority", row["boundary"])

    def test_28_accessibility_remains_reserved(self) -> None:
        self.assertFalse(self.accessibility["accessibility_complete"])
        for key in (
            "manual_browser_evaluation",
            "keyboard_evaluation",
            "screen_reader_evaluation",
            "form_alternative_affected_user_evaluation",
        ):
            self.assertEqual(self.accessibility[key], "reserved")

    def test_29_accessible_report_structure(self) -> None:
        text = (PHASE / "x2/accessible-static-report.html").read_text(encoding="utf-8")
        for token in (
            '<html lang="en-NZ">',
            "<main",
            "<h1>",
            "<h2",
            "<table>",
            "<caption>",
            'scope="col"',
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(token, text)
        self.assertNotIn("<script", text.lower())

    def test_30_environment_changed_no_host_state(self) -> None:
        self.assertFalse(self.environment["codex_desktop_updated"])
        self.assertFalse(self.environment["host_security_changed"])
        self.assertFalse(self.environment["windows_features_changed"])
        self.assertFalse(self.environment["rebooted"])
        self.assertTrue(self.environment["version_verification_only"])

    def test_31_threat_model_does_not_overclaim(self) -> None:
        self.assertEqual(self.threats["planned_threat_count"], 12)
        self.assertEqual(self.threats["control_witness_count"], 12)
        self.assertFalse(self.threats["complete_privacy_claim"])
        self.assertFalse(self.threats["complete_accessibility_claim"])
        self.assertFalse(self.threats["exhaustive_security_claim"])

    def test_32_wellbeing_is_bounded(self) -> None:
        self.assertTrue(self.wellbeing["relational_only"])
        self.assertTrue(self.wellbeing["workload"]["single_sparse_lane"])
        self.assertTrue(self.wellbeing["workload"]["pause_right_preserved"])
        self.assertTrue(self.wellbeing["hamish_may_pause_redirect_rename_or_stop"])

    def test_33_reproduction_is_same_owner_only(self) -> None:
        self.assertTrue(self.reproduction["same_owner_reproduction"])
        self.assertFalse(self.reproduction["independent_team_reproduction"])
        self.assertFalse(self.reproduction["external_audit"])
        self.assertFalse(self.reproduction["full_repository_suite"])

    def test_34_stage20_remains_not_ready(self) -> None:
        self.assertEqual(self.stage20["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(all(value == 0 for value in self.stage20["evidence_vector"].values()))

    def test_35_all_phase_json_strictly_parse(self) -> None:
        for path in sorted(PHASE.rglob("*.json")):
            strict_json(path)

    def test_36_no_x1_file_modified(self) -> None:
        result = subprocess.run(
            ["git", "diff", "--quiet", X1_HEAD, "--", "docs/orin-thale/v665-v1/x1"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 0)

    def test_37_no_raw_identifier_or_private_absolute_path(self) -> None:
        raw_identifier = re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        )
        private_path = re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]")
        paths = [
            *PHASE.rglob("*"),
            ROOT / "scripts/build_ghc_family_v665_v1_evidence.py",
            ROOT / "scripts/ghc_family_v665_v1_runner_core.py",
            *[ROOT / "scripts" / name for name in (
                "ghc_family_variational_bicomplex_boundary.py",
                "ghc_family_jet_atlas_quarantine.py",
                "ghc_family_contact_degree_guard.py",
                "ghc_family_euler_boundary_lineage.py",
                "ghc_family_millinery_topology_vacancy.py",
                "ghc_family_millinery_material_state.py",
                "ghc_family_thos_bench_handover.py",
                "ghc_family_freed_id_work_envelope.py",
                "ghc_family_millinery_rights_authority.py",
                "ghc_family_stage20_model_nonpromotion.py",
            )],
            Path(__file__),
        ]
        for path in sorted(set(paths)):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(raw_identifier.search(text), str(path))
                self.assertIsNone(private_path.search(text), str(path))

    def test_38_owner_growth_and_words_below_caps(self) -> None:
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        words = 0
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
                words += len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
        self.assertLess(len(files), 2_000)
        self.assertLessEqual(words, 100_000)


if __name__ == "__main__":
    unittest.main()
