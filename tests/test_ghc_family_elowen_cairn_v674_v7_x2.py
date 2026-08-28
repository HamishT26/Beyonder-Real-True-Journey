"""Owner-scoped tests for Elowen Cairn v674-v7 x2 evidence."""

from __future__ import annotations

import hashlib
import importlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts.ghc_family_elowen_v674_v7_registration_handover_lineage import (
    HandoverError,
    positive_fixture as handover_fixture,
    rejecting_fixtures as handover_rejecting,
    validate_record,
)
from scripts.ghc_family_elowen_v674_v7_instrument_topology_contract import (
    ObservationContractError,
    positive_fixture as observation_fixture,
    rejecting_fixtures as observation_rejecting,
    validate_contract,
)
from scripts.ghc_family_elowen_v674_v7_registration_guard import (
    EvidenceGuardError,
    canonical_json_bytes,
    run_named_guard,
    validate_proposal,
)


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v674-v7"
SOURCE_FINAL = "c7412530cbb3a549ad681ae7b98c29b64e31ad4d"
X1_COMMIT = "d293bfaefa278b1d2e5bd086c25625df30dbe3e9"
BRANCH = "codex/GHC-Family/elowen-cairn-v674-v7-full-tools"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
RUNNER_MODULES = [
    "ghc_family_astrolabe_topology",
    "ghc_family_astrolabe_abstention",
    "ghc_family_music_box_topology",
    "ghc_family_music_box_abstention",
    "ghc_family_kaleidoscope_topology",
    "ghc_family_kaleidoscope_abstention",
    "ghc_family_instrument_registration_provenance",
    "ghc_family_instrument_privacy_access",
    "ghc_family_gmut_thos_instrument_boundary",
    "ghc_family_instrument_workload_handover",
]


def load(relative: str) -> dict:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True
    ).stdout.decode("utf-8", errors="strict").strip()


class ElowenCairnV674V7X2Tests(unittest.TestCase):
    def test_01_exact_branch_and_x1_ancestry(self) -> None:
        self.assertEqual(git_text("branch", "--show-current"), BRANCH)
        self.assertEqual(git_text("rev-parse", f"{X1_COMMIT}^"), SOURCE_FINAL)
        self.assertEqual(
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", X1_COMMIT, "HEAD"], cwd=ROOT
            ).returncode,
            0,
        )

    def test_02_x1_manifest_replays_at_immutable_commit(self) -> None:
        manifest = json.loads(
            subprocess.run(
                [
                    "git",
                    "show",
                    f"{X1_COMMIT}:docs/elowen-cairn/v674-v7/validation/x1-manifest.json",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout.decode("utf-8")
        )
        self.assertEqual(manifest["entry_count"], 20)
        for entry in manifest["entries"]:
            blob = subprocess.run(
                ["git", "show", f"{X1_COMMIT}:{entry['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_03_x1_frozen_paths_remain_unchanged(self) -> None:
        changed = git_text(
            "diff",
            "--name-only",
            X1_COMMIT,
            "--",
            "docs/elowen-cairn/v674-v7/x1",
            "scripts/build_ghc_family_elowen_cairn_v674_v7_x1.py",
            "tests/test_ghc_family_elowen_cairn_v674_v7_x1.py",
        )
        self.assertEqual(changed, "")

    def test_04_outcome_ledger_uses_only_four_labels(self) -> None:
        ledger = load("x2/outcome-ledger.json")
        self.assertEqual(ledger["counts"], OUTCOMES)
        self.assertEqual(len(ledger["rows"]), 60)
        self.assertEqual(Counter(row["observed_outcome"] for row in ledger["rows"]), Counter(OUTCOMES))
        self.assertEqual(
            {row["observed_outcome"] for row in ledger["rows"]}, set(OUTCOMES)
        )

    def test_05_all_preregistered_mutations_executed_and_rejected(self) -> None:
        receipt = load("x2/mutation-receipt.json")
        self.assertEqual(receipt["preregistered"], 240)
        self.assertEqual(receipt["executed"], 240)
        self.assertEqual(receipt["rejected"], 240)
        self.assertEqual(receipt["unexpected_accepts"], 0)
        self.assertEqual(receipt["completion_credit"], 0)
        self.assertTrue(all(row["rejected"] for row in receipt["rows"]))

    def test_06_mutation_matrix_is_four_per_proposal_and_unique(self) -> None:
        rows = load("x2/mutation-receipt.json")["rows"]
        self.assertEqual(len({row["mutation_id"] for row in rows}), 240)
        counts = Counter(row["proposal_id"] for row in rows)
        self.assertEqual(set(counts.values()), {4})
        self.assertEqual(
            {row["mutation"] for row in rows},
            {
                "missing_hypothesis",
                "invalid_outcome_label",
                "external_action_promotion",
                "missing_protected_gates",
            },
        )

    def test_07_positive_controls_cover_completed_and_represented_only(self) -> None:
        receipt = load("x2/positive-control-receipt.json")
        self.assertEqual((receipt["planned"], receipt["executed"], receipt["passed"]), (54, 54, 54))
        self.assertTrue(all(row["accepted"] and row["external_actions"] == 0 for row in receipt["rows"]))

    def test_08_open_gaps_and_exact_gates_have_no_positive_control(self) -> None:
        rows = load("x2/outcome-ledger.json")["rows"]
        held = [row for row in rows if row["observed_outcome"] in {"open_gap", "exact_gate"}]
        self.assertEqual(len(held), 6)
        self.assertTrue(all(row["positive_control"] is None for row in held))

    def test_09_tool_evidence_has_three_tools_and_paired_rejections(self) -> None:
        receipt = load("x2/tool-evidence.json")
        self.assertEqual(len(receipt["tools"]), 3)
        self.assertEqual(receipt["observation_vacancy"]["rejecting"], 5)
        self.assertEqual(receipt["handover_lineage"]["rejecting"], 5)
        self.assertTrue(receipt["registration_guard"]["duplicate_rejected"])
        self.assertTrue(receipt["registration_guard"]["nonfinite_rejected"])
        self.assertEqual(receipt["external_actions"], 0)

    def test_10_canonical_json_rejects_duplicate_and_nonfinite_values(self) -> None:
        self.assertEqual(canonical_json_bytes({"b": 2, "a": 1}), b'{"a":1,"b":2}')
        with self.assertRaises(EvidenceGuardError):
            canonical_json_bytes('{"a":1,"a":2}')
        with self.assertRaises(EvidenceGuardError):
            canonical_json_bytes('{"value":NaN}')

    def test_11_observation_vacancy_accepts_three_synthetic_lenses(self) -> None:
        for lens in ("astrolabe", "music_box", "kaleidoscope"):
            row = validate_contract(observation_fixture(lens))
            self.assertTrue(row["accepted"])
            self.assertEqual(row["real_measurements"], 0)
            self.assertIsNone(row["component_count"])
            self.assertIsNone(row["length_m"])
            self.assertIsNone(row["material_composition"])

    def test_12_observation_vacancy_rejects_five_promotions(self) -> None:
        rows = observation_rejecting()
        self.assertEqual(len(rows), 5)
        for row in rows:
            with self.assertRaises(ObservationContractError):
                validate_contract(row)

    def test_13_handover_lineage_accepts_three_synthetic_lenses(self) -> None:
        for lens in ("astrolabe", "music_box", "kaleidoscope"):
            row = validate_record(handover_fixture(lens))
            self.assertTrue(row["accepted"])
            self.assertFalse(row["real_operator"])
            self.assertEqual([event["sequence"] for event in row["events"]], [1, 2, 3, 4])

    def test_14_handover_lineage_rejects_five_promotions(self) -> None:
        rows = handover_rejecting()
        self.assertEqual(len(rows), 5)
        for row in rows:
            with self.assertRaises(HandoverError):
                validate_record(row)

    def test_15_runner_evidence_records_ten_passes(self) -> None:
        receipt = load("x2/runner-evidence.json")
        self.assertEqual((receipt["planned"], receipt["built_new"], receipt["executed"], receipt["passed"]), (10, 10, 10, 10))
        self.assertFalse(receipt["global_install"])
        self.assertTrue(all(row["accepted"] for row in receipt["rows"]))

    def test_16_runner_modules_emit_typed_zero_action_receipts(self) -> None:
        for module_name in RUNNER_MODULES:
            module = importlib.import_module(f"scripts.{module_name}")
            receipt = module.build_receipt()
            self.assertTrue(receipt["accepted"])
            self.assertEqual(receipt["external_actions"], 0)
            self.assertEqual(receipt["real_people"], 0)
            self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_17_skill_evidence_records_twenty_validated_smokes(self) -> None:
        receipt = load("x2/skill-evidence.json")
        self.assertEqual(receipt["initialized_with_official_creator"], 20)
        self.assertEqual((receipt["built"], receipt["quick_validated"], receipt["smoke_used"]), (20, 20, 20))
        self.assertFalse(receipt["global_install"])
        self.assertTrue(all(row["quick_validated"] and row["smoke_used"] for row in receipt["rows"]))

    def test_18_skill_files_are_customized_and_boundary_complete(self) -> None:
        rows = load("x2/skill-evidence.json")["rows"]
        self.assertEqual(len(rows), 20)
        for row in rows:
            text = (ROOT / row["skill_path"]).read_text(encoding="utf-8")
            agent = (ROOT / row["agent_path"]).read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname:"))
            self.assertIn("description:", text)
            self.assertIn("## Workflow", text)
            self.assertIn("## Boundary", text)
            self.assertNotIn("[TODO", text)
            self.assertIn("default_prompt:", agent)

    def test_19_portfolio_counts_are_exact(self) -> None:
        payload = load("x2/portfolio-outcome.json")
        self.assertEqual(
            payload["counts"],
            {
                "inherited_reviews": 60,
                "safe_now": 120,
                "candidates": 80,
                "exact_approval": 20,
                "blocked": 10,
                "skills": 20,
                "runners": 10,
                "clean_fix_refine": 100,
                "successor_skills": 10,
                "successor_runners": 10,
                "successor_clean_fix_refine": 60,
                "successor_seeds": 60,
            },
        )
        self.assertEqual(payload["inherited_completion_credit"], 0)

    def test_20_exact_and_blocked_work_remains_unexecuted(self) -> None:
        payload = load("x2/exact-and-blocked-register.json")
        self.assertEqual(len(payload["exact_approval"]), 20)
        self.assertEqual(len(payload["blocked"]), 10)
        self.assertEqual(payload["executed"], 0)
        self.assertTrue(all(row["x2_state"] == "held_unexecuted" for row in payload["exact_approval"] + payload["blocked"]))

    def test_21_clean_fix_refine_and_successor_seeds_preserve_credit_boundary(self) -> None:
        payload = load("x2/clean-fix-refine-evidence.json")
        self.assertEqual(len(payload["completed"]), 100)
        self.assertEqual(len(payload["successor_recommendations"]), 60)
        self.assertTrue(all(row["x2_state"] == "recommendation_only" for row in payload["successor_recommendations"]))
        self.assertEqual(payload["destructive_cleanup"], 0)
        self.assertEqual(payload["sibling_mutation"], 0)

    def test_22_method_flow_retains_all_failures_and_recoveries(self) -> None:
        ledger = load("x2/method-flow-evidence.json")
        self.assertEqual(ledger["counts"]["methods"], 289)
        self.assertEqual(ledger["counts"]["witnesses"], 545)
        self.assertEqual(ledger["counts"]["state_events"], 867)
        self.assertEqual(ledger["counts"]["recommendations"], 289)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 256, "pass": 289})
        self.assertEqual(sum("EC6747-X2-" in value for row in ledger["methods"] for value in row["retained_negative_ids"]), 2)
        self.assertTrue(any("EC6747-X2-N001" in row["retained_negative_ids"] for row in ledger["methods"]))

    def test_23_effective_counts_are_additive_and_do_not_rewrite_tamar(self) -> None:
        overlay = load("x2/method-flow-evidence.json")["effective_overlay"]
        self.assertEqual(
            overlay,
            {
                "effective_negatives": 39647,
                "effective_methods": 27866,
                "failed_witnesses": 11308,
                "bounded_passing_witnesses": 15149,
                "repository_seal_rewritten": False,
            },
        )

    def test_24_phase_truth_preserves_gaps_gates_and_terminal_verdict(self) -> None:
        truth = load("x2/phase-truth-evidence.json")
        self.assertEqual(truth["proposal_chain_before"], 6910)
        self.assertEqual(truth["proposal_chain_after"], 6970)
        self.assertEqual(truth["open_gaps"], 328)
        self.assertEqual(truth["exact_gates"], 321)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_world_actions"], 0)
        self.assertEqual(truth["external_writes"], 0)

    def test_25_sources_supply_vocabulary_only(self) -> None:
        ledger = load("x2/source-evidence-ledger.json")
        self.assertEqual(len(ledger["rows"]), 6)
        self.assertEqual(ledger["network_dataset_or_api_calls_in_execution"], 0)
        self.assertEqual(ledger["dataset_or_media_downloads_in_execution"], 0)
        self.assertEqual(ledger["real_rows"], 0)
        self.assertFalse(ledger["citations_are_observations"])
        self.assertFalse(ledger["authority_conferred"])

    def test_26_public_x2_documents_have_no_private_payload_identifiers(self) -> None:
        patterns = [
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
            re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
            re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
            re.compile(r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I),
        ]
        for path in (OWNER_ROOT / "x2").rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".yaml", ".txt"}:
                text = path.read_text(encoding="utf-8")
                self.assertFalse(any(pattern.search(text) for pattern in patterns), path)

    def test_27_accessible_report_has_static_structure_and_reserved_manual_review(self) -> None:
        text = (OWNER_ROOT / "x2" / "accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('href="#main"', '<main id="main">', '<caption>', 'scope="col"', "@media(max-width", "a:focus"):
            self.assertIn(token, text)
        self.assertIn("assistive-technology", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_28_environment_verification_changed_nothing(self) -> None:
        receipt = load("x2/environment-receipt.json")
        self.assertEqual(receipt["version_verification"], "read_only_scalar_probes")
        for key in (
            "desktop_updated",
            "elevation",
            "host_security_changes",
            "windows_feature_changes",
            "sandbox_or_hyper_v_activated",
            "unrelated_installation",
            "reboot",
        ):
            self.assertFalse(receipt[key])
        self.assertEqual(receipt["real_data_downloads"], 0)

    def test_29_evidence_validation_receipts_are_exact_and_valid(self) -> None:
        review = load("validation/evidence-staged-review.json")
        manifest = load("validation/evidence-manifest.json")
        method = load("validation/evidence-method-flow-validation.json")
        validation = load("validation/evidence-validation-receipt.json")
        privacy = load("validation/evidence-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["x1_frozen_path_mutations"], [])
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_git_blob")
        self.assertTrue(method["valid"])
        self.assertEqual(method["issue_count"], 0)
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["json_issues"], [])
        self.assertEqual(validation["python_compile_issues"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_30_no_closeout_final_seal_or_route_delivery_exists(self) -> None:
        for name in ("closeout", "final", "seal", "handoffs"):
            self.assertFalse((OWNER_ROOT / name).exists())
        route = load("x1/route-plan.json")
        self.assertEqual(route["delivery_state"], "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH")
        self.assertEqual(route["successor_contact_count"], 0)
        self.assertEqual(route["task_creation_count"], 0)


if __name__ == "__main__":
    unittest.main()
