"""Dependency-closed tests for Ilyra Fen v664-v5 x2 evidence."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_structural_monitoring_evidence as monitoring  # noqa: E402
import ghc_family_freed_id_flashcards as flashcards  # noqa: E402


PHASE = ROOT / "docs/ilyra-fen/v664-v5"
X1 = "cfbca99a371f97eecb959fb92be3469c0861ddf3"
DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_structural_monitoring_evidence.py",
    "scripts/ghc_family_freed_id_flashcards.py",
    "docs/ilyra-fen/v664-v5/x1/phase-charter.json",
    "docs/ilyra-fen/v664-v5/x1/proposal-freeze.json",
    "docs/ilyra-fen/v664-v5/x1/portfolio-freeze.json",
    "docs/ilyra-fen/v664-v5/x1/flashcard-architecture-freeze.json",
    "docs/ilyra-fen/v664-v5/x1/source-verification.json",
]


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class StructuralMonitoringEvidenceTests(unittest.TestCase):
    def test_registry_has_exactly_twenty_unique_surfaces(self) -> None:
        self.assertEqual(len(monitoring.SURFACE_SPECS), 20)
        self.assertEqual(len(monitoring.SPEC_BY_SLUG), 20)
        self.assertEqual(len(monitoring.SPEC_BY_ID), 20)

    def test_only_four_core_outcomes_are_present(self) -> None:
        self.assertEqual({row["expected_outcome"] for row in monitoring.SURFACE_SPECS}, monitoring.ALLOWED_OUTCOMES)

    def test_frozen_outcome_distribution(self) -> None:
        self.assertEqual(Counter(row["expected_outcome"] for row in monitoring.SURFACE_SPECS), Counter(completed=14, represented=4, open_gap=1, exact_gate=1))

    def test_all_one_hundred_mutations_are_rejected(self) -> None:
        result = monitoring.ghc_family_execute_v664_v5()
        self.assertEqual(result["mutation_count"], 100)
        self.assertEqual(result["rejected_mutation_count"], 100)

    def test_every_fixture_retains_all_protected_refusals(self) -> None:
        for frozen in monitoring.SURFACE_SPECS:
            fixture = monitoring.ghc_family_build_structural_monitoring_fixture(frozen["surface"])
            self.assertTrue(all(fixture[field] is False for field in monitoring.REFUSAL_FIELDS))
            self.assertEqual(fixture["protected_gates"], list(monitoring.PROTECTED_GATES))

    def test_every_fixture_has_zero_real_world_rows_and_no_authority(self) -> None:
        for frozen in monitoring.SURFACE_SPECS:
            fixture = monitoring.ghc_family_build_structural_monitoring_fixture(frozen["surface"])
            self.assertEqual(fixture["real_world_rows"], 0)
            self.assertEqual(fixture["authority"], "none")
            self.assertTrue(fixture["synthetic"])

    def test_open_gap_is_the_zero_row_adapter_only(self) -> None:
        self.assertEqual([row["surface"] for row in monitoring.SURFACE_SPECS if row["expected_outcome"] == "open_gap"], ["zero-row-nsmp-adapter"])

    def test_exact_gate_is_the_authority_matrix_only(self) -> None:
        self.assertEqual([row["surface"] for row in monitoring.SURFACE_SPECS if row["expected_outcome"] == "exact_gate"], ["structural-safety-authority-matrix"])

    def test_stage_20_surface_is_a_completed_refusal_not_readiness(self) -> None:
        fixture = monitoring.ghc_family_build_structural_monitoring_fixture("stage20-strong-motion-refusal")
        self.assertEqual(fixture["expected_outcome"], "completed")
        self.assertFalse(fixture["stage_20_ready"])
        self.assertEqual(fixture["admitted_evidence_rows"], 0)

    def test_unknown_surface_is_rejected(self) -> None:
        with self.assertRaises(monitoring.EvidenceError):
            monitoring.ghc_family_build_structural_monitoring_fixture("unknown")

    def test_missing_key_is_rejected(self) -> None:
        fixture = monitoring.ghc_family_build_structural_monitoring_fixture("sensor-array-topology")
        fixture.pop("authority")
        with self.assertRaises(monitoring.EvidenceError):
            monitoring.ghc_family_validate_structural_monitoring_surface(fixture)

    def test_extra_key_is_rejected(self) -> None:
        fixture = monitoring.ghc_family_build_structural_monitoring_fixture("sensor-array-topology")
        fixture["extra"] = True
        with self.assertRaises(monitoring.EvidenceError):
            monitoring.ghc_family_validate_structural_monitoring_surface(fixture)

    def test_protected_gate_promotion_is_rejected(self) -> None:
        fixture = monitoring.ghc_family_build_structural_monitoring_fixture("sensor-array-topology")
        fixture["professional_authority"] = True
        with self.assertRaises(monitoring.EvidenceError):
            monitoring.ghc_family_validate_structural_monitoring_surface(fixture)

    def test_source_map_drift_is_rejected(self) -> None:
        fixture = monitoring.ghc_family_build_structural_monitoring_fixture("sensor-array-topology")
        fixture["source_ids"] = ["SRC-DRIFT"]
        with self.assertRaises(monitoring.EvidenceError):
            monitoring.ghc_family_validate_structural_monitoring_surface(fixture)

    def test_phase_execution_is_network_download_and_waveform_free(self) -> None:
        result = monitoring.ghc_family_execute_v664_v5()
        self.assertEqual((result["network_calls"], result["downloads"], result["waveform_reads"], result["real_world_rows"]), (0, 0, 0, 0))

    def test_phase_aliases_are_additive_and_callable(self) -> None:
        self.assertIs(monitoring.build_ghc_family_v664_v5_evidence, monitoring.ghc_family_execute_v664_v5)
        self.assertIs(monitoring.ghc_family_validate_v664_v5_surface, monitoring.ghc_family_validate_structural_monitoring_surface)

    def test_fixture_serialization_is_deterministic(self) -> None:
        first = monitoring.ghc_family_build_structural_monitoring_fixture("stationxml-response-completeness")
        second = monitoring.ghc_family_build_structural_monitoring_fixture("stationxml-response-completeness")
        self.assertEqual(monitoring.digest(first), monitoring.digest(second))

    def test_validator_does_not_mutate_fixture(self) -> None:
        fixture = monitoring.ghc_family_build_structural_monitoring_fixture("missingness-saturation-dropout")
        before = deepcopy(fixture)
        monitoring.ghc_family_validate_structural_monitoring_surface(fixture)
        self.assertEqual(fixture, before)

    def test_runner_registry_has_ten_profiles_with_exact_coverage(self) -> None:
        covered = [surface for values in monitoring.RUNNER_PROFILES.values() for surface in values]
        self.assertEqual(len(monitoring.RUNNER_PROFILES), 10)
        self.assertEqual(Counter(covered), Counter(monitoring.SPEC_BY_SLUG.keys()))

    def test_unknown_runner_profile_is_rejected(self) -> None:
        with self.assertRaises(monitoring.EvidenceError):
            monitoring.ghc_family_run_structural_monitoring_profile("unknown")

    def test_cli_single_profile_is_valid(self) -> None:
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "ghc_family_structural_monitoring_evidence.py"), "--profile", "terminal-refusal"], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])


def surface_test(surface: str):
    def test(self: StructuralMonitoringEvidenceTests) -> None:
        result = monitoring.ghc_family_execute_structural_monitoring_surface(surface)
        self.assertTrue(result["valid"])
        self.assertEqual(result["mutation_count"], 5)
        self.assertEqual(result["rejected_mutation_count"], 5)
        self.assertFalse(result["post_success_replay"])
    return test


def runner_test(profile: str):
    def test(self: StructuralMonitoringEvidenceTests) -> None:
        result = monitoring.ghc_family_run_structural_monitoring_profile(profile)
        self.assertTrue(result["valid"])
        self.assertEqual(result["network_calls"], 0)
        self.assertEqual(result["waveform_reads"], 0)
    return test


for _surface in monitoring.SPEC_BY_SLUG:
    setattr(StructuralMonitoringEvidenceTests, f"test_surface_{_surface.replace('-', '_')}", surface_test(_surface))
for _profile in monitoring.RUNNER_PROFILES:
    setattr(StructuralMonitoringEvidenceTests, f"test_runner_{_profile.replace('-', '_')}", runner_test(_profile))


class FlashcardRemasterTests(unittest.TestCase):
    def model(self) -> dict:
        return flashcards.build_model(PHASE, X1)

    def test_model_uses_current_owner_and_phase(self) -> None:
        model = self.model()
        self.assertEqual(model["index"]["owner"], "Ilyra Fen")
        self.assertEqual(model["index"]["phase"], "v664-v5")

    def test_model_has_dynamic_exact_tier_counts(self) -> None:
        model = self.model()
        self.assertEqual(model["index"]["expected_tier_counts"], {"1": 1, "2": 3, "3": 1, "4": 248})
        self.assertEqual(model["index"]["card_count"], 253)

    def test_model_preserves_four_outcomes(self) -> None:
        self.assertEqual(self.model()["index"]["new_core_outcomes"], {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4})

    def test_model_route_is_current_and_unsent(self) -> None:
        model = self.model()
        self.assertEqual(model["index"]["current_route"], {"owner": "Ilyra Fen", "phase": "v664-v5"})
        self.assertEqual(model["index"]["successor_route"], {"owner": "Auren Lark", "phase": "v664-v6", "contacted": False})

    def test_compact_pointer_is_prepared_and_unsent(self) -> None:
        text = flashcards.compact_message(self.model())
        self.assertIn("PREPARED_NOT_SENT = true", text)
        self.assertIn("SENT = false", text)
        self.assertNotIn("completed terminal gate", text)
        self.assertEqual(flashcards.private_candidates(text), [])

    def test_accessible_report_uses_dynamic_labels(self) -> None:
        report = flashcards.accessible_report(self.model())
        self.assertIn("Ilyra Fen", report)
        self.assertIn("v664-v5", report)
        self.assertIn('<main id="main">', report)
        self.assertIn("<caption>", report)

    def test_invalid_x1_shape_is_rejected(self) -> None:
        with self.assertRaises(flashcards.FlashcardError):
            flashcards.build_model(PHASE, "not-a-git-object")

    def test_private_candidate_detector_covers_five_classes(self) -> None:
        samples = [
            "123e4567-" + "e89b-12d3-a456-426614174000",
            "C:" + "\\Users\\private\\file",
            '"pass' + 'word": "secret"',
            "code" + "x://private",
            '"raw_' + 'transcript": "x"',
        ]
        self.assertEqual(sum(bool(flashcards.private_candidates(value)) for value in samples), 5)

    def test_loaded_deck_validates(self) -> None:
        result = flashcards.validate_deck(ROOT, "docs/ilyra-fen/v664-v5/deck")
        self.assertTrue(result["valid"])
        self.assertEqual(result["model"]["card_count"], 253)

    def test_loaded_deck_manifest_replays(self) -> None:
        deck, _ = flashcards.load_deck(ROOT, "docs/ilyra-fen/v664-v5/deck")
        result = flashcards.manifest_status(deck)
        self.assertTrue(result["valid"])
        self.assertEqual(result["expected_entries"], result["observed_entries"])

    def test_loaded_deck_privacy_scan_is_clear(self) -> None:
        deck, _ = flashcards.load_deck(ROOT, "docs/ilyra-fen/v664-v5/deck")
        result = flashcards.privacy_status(deck)
        self.assertTrue(result["valid"])
        self.assertEqual(result["candidate_count"], 0)

    def test_deck_mutations_all_reject(self) -> None:
        result = flashcards.mutation_receipt(ROOT, "docs/ilyra-fen/v664-v5/deck")
        self.assertEqual(result["mutation_count"], 60)
        self.assertEqual(result["rejected_count"], 60)
        self.assertTrue(result["valid"])

    def test_wrong_output_directory_is_rejected(self) -> None:
        with self.assertRaises(flashcards.FlashcardError):
            flashcards.build_outputs(ROOT, "docs/ilyra-fen/v664-v5", "docs/ilyra-fen/v664-v5/not-deck", X1)

    def test_dangling_output_symlink_is_rejected_without_escape(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ilyra-link-regression-") as directory:
            root = Path(directory)
            inside = root / "inside"
            outside = root / "outside"
            inside.mkdir()
            outside.mkdir()
            target = outside / "escaped.bin"
            link = inside / "artifact.bin"
            link.symlink_to(target)
            with self.assertRaises(flashcards.FlashcardError):
                flashcards.write_equal_or_new(link, b"bounded-proof")
            self.assertFalse(target.exists())

    def test_card_owner_is_dynamic_everywhere(self) -> None:
        self.assertEqual({row["owner"] for row in self.model()["cards"]}, {"Ilyra Fen"})

    def test_portfolio_dispositions_come_from_frozen_rows(self) -> None:
        cards = self.model()["cards"]
        skill_cards = [row for row in cards if row.get("content", {}).get("program_class") == "owner_skill_ideas"]
        self.assertEqual(len(skill_cards), 10)
        self.assertEqual({row["outcome"] for row in skill_cards}, {"completed"})


class MaterializedEvidenceTests(unittest.TestCase):
    def test_phase_truth_exact_counts(self) -> None:
        truth = load("x2/phase-truth.json")
        self.assertEqual(truth["new_outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertTrue(truth["valid"])

    def test_negative_register_reconciles(self) -> None:
        record = load("x2/retained-negative-register.json")
        self.assertEqual(record["effective_negatives"], 24672)
        self.assertEqual(len(record["new_records"]), 105)
        self.assertTrue(record["no_negative_erased"])

    def test_method_flow_reconciles(self) -> None:
        record = load("x2/method-flow-state.json")
        self.assertEqual(record["effective_methods"], 8866)
        self.assertEqual(len(record["methods"]), 25)
        self.assertTrue(record["no_failure_erased"])

    def test_gate_register_remains_open(self) -> None:
        record = load("x2/open-gate-register.json")
        self.assertEqual((record["effective_open_gaps"], record["effective_exact_gates"]), (171, 169))
        self.assertEqual(record["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_surface_artifact_triplets_exist(self) -> None:
        for frozen in monitoring.SURFACE_SPECS:
            base = PHASE / "x2" / "surfaces" / frozen["surface"]
            self.assertEqual({path.name for path in base.iterdir()}, {"contract.json", "mutation-results.json", "bounded-receipt.json"})

    def test_ten_skill_packages_are_phase_local(self) -> None:
        skills = sorted((PHASE / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        self.assertTrue(all((path.parent / "smoke-receipt.json").is_file() for path in skills))

    def test_ten_runner_receipts_exist(self) -> None:
        self.assertEqual(len(list((PHASE / "x2" / "runners").glob("*.json"))), 10)

    def test_portfolio_counts_match_freeze(self) -> None:
        frozen = load("x1/portfolio-freeze.json")["counts"]
        executed = load("x2/portfolio-execution.json")["counts"]
        self.assertEqual(executed, frozen)

    def test_successor_is_not_contacted(self) -> None:
        self.assertFalse(load("x2/successor-recommendations.json")["contacted"])
        self.assertEqual(load("x2/successor-recommendations.json")["execution_credit"], 0)

    def test_x1_immutability_receipt_is_exact(self) -> None:
        record = load("x2/x1-immutability-receipt.json")
        self.assertEqual(record["x1"], X1)
        self.assertEqual(record["working_x1_changes"], [])


if __name__ == "__main__":
    unittest.main()
