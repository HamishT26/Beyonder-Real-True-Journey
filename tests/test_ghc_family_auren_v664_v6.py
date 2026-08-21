"""Dependency-closed tests for Auren Lark v664-v6 x2 evidence."""

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

import ghc_family_ocean_profile_evidence as ocean  # noqa: E402
import ghc_family_auren_flashcards as flashcards  # noqa: E402


PHASE = ROOT / "docs/auren-lark/v664-v6"
X1 = "0732e8d3ba44e04a4729ffed1a33f09109eb6cea"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class OceanProfileEvidenceTests(unittest.TestCase):
    def test_registry_has_twenty_unique_surfaces(self) -> None:
        self.assertEqual((len(ocean.SURFACE_SPECS), len(ocean.SPEC_BY_SLUG), len(ocean.SPEC_BY_ID)), (20, 20, 20))

    def test_only_four_outcomes_are_present(self) -> None:
        self.assertEqual({row["expected_outcome"] for row in ocean.SURFACE_SPECS}, ocean.ALLOWED_OUTCOMES)

    def test_frozen_outcome_distribution(self) -> None:
        self.assertEqual(Counter(row["expected_outcome"] for row in ocean.SURFACE_SPECS), Counter(completed=14, represented=4, open_gap=1, exact_gate=1))

    def test_all_one_hundred_mutations_reject(self) -> None:
        result = ocean.ghc_family_execute_v664_v6()
        self.assertEqual((result["mutation_count"], result["rejected_mutation_count"]), (100, 100))

    def test_every_fixture_retains_refusals(self) -> None:
        for row in ocean.SURFACE_SPECS:
            fixture = ocean.ghc_family_build_ocean_profile_fixture(row["surface"])
            self.assertTrue(all(fixture[field] is False for field in ocean.REFUSAL_FIELDS))
            self.assertEqual(fixture["protected_gates"], list(ocean.PROTECTED_GATES))

    def test_every_fixture_is_zero_row_and_authority_free(self) -> None:
        for row in ocean.SURFACE_SPECS:
            fixture = ocean.ghc_family_build_ocean_profile_fixture(row["surface"])
            self.assertTrue(fixture["synthetic"])
            self.assertEqual((fixture["real_world_rows"], fixture["authority"]), (0, "none"))

    def test_open_gap_is_zero_row_adapter(self) -> None:
        self.assertEqual([row["surface"] for row in ocean.SURFACE_SPECS if row["expected_outcome"] == "open_gap"], ["zero-row-argo-adapter"])

    def test_exact_gate_is_authority_matrix(self) -> None:
        self.assertEqual([row["surface"] for row in ocean.SURFACE_SPECS if row["expected_outcome"] == "exact_gate"], ["ocean-observation-authority-matrix"])

    def test_terminal_refusal_withholds_stage20(self) -> None:
        fixture = ocean.ghc_family_build_ocean_profile_fixture("stage20-ocean-profile-refusal")
        self.assertEqual(fixture["expected_outcome"], "completed")
        self.assertFalse(fixture["stage_20_ready"])
        self.assertEqual(fixture["admitted_evidence_rows"], 0)

    def test_unknown_surface_rejects(self) -> None:
        with self.assertRaises(ocean.EvidenceError):
            ocean.ghc_family_build_ocean_profile_fixture("unknown")

    def test_missing_key_rejects(self) -> None:
        fixture = ocean.ghc_family_build_ocean_profile_fixture("float-cycle-metadata-topology")
        fixture.pop("authority")
        with self.assertRaises(ocean.EvidenceError):
            ocean.ghc_family_validate_ocean_profile_surface(fixture)

    def test_extra_key_rejects(self) -> None:
        fixture = ocean.ghc_family_build_ocean_profile_fixture("float-cycle-metadata-topology")
        fixture["extra"] = True
        with self.assertRaises(ocean.EvidenceError):
            ocean.ghc_family_validate_ocean_profile_surface(fixture)

    def test_refusal_promotion_rejects(self) -> None:
        fixture = ocean.ghc_family_build_ocean_profile_fixture("float-cycle-metadata-topology")
        fixture["professional_authority"] = True
        with self.assertRaises(ocean.EvidenceError):
            ocean.ghc_family_validate_ocean_profile_surface(fixture)

    def test_source_drift_rejects(self) -> None:
        fixture = ocean.ghc_family_build_ocean_profile_fixture("float-cycle-metadata-topology")
        fixture["source_ids"] = ["SRC-DRIFT"]
        with self.assertRaises(ocean.EvidenceError):
            ocean.ghc_family_validate_ocean_profile_surface(fixture)

    def test_no_network_download_or_profile_rows(self) -> None:
        result = ocean.ghc_family_execute_v664_v6()
        self.assertEqual((result["network_calls"], result["downloads"], result["profile_rows"], result["real_world_rows"]), (0, 0, 0, 0))

    def test_phase_aliases_are_additive(self) -> None:
        self.assertIs(ocean.build_ghc_family_v664_v6_evidence, ocean.ghc_family_execute_v664_v6)
        self.assertIs(ocean.ghc_family_validate_v664_v6_surface, ocean.ghc_family_validate_ocean_profile_surface)

    def test_serialization_is_deterministic(self) -> None:
        first = ocean.ghc_family_build_ocean_profile_fixture("qc-flag-lineage")
        second = ocean.ghc_family_build_ocean_profile_fixture("qc-flag-lineage")
        self.assertEqual(ocean.digest(first), ocean.digest(second))

    def test_validator_does_not_mutate_fixture(self) -> None:
        fixture = ocean.ghc_family_build_ocean_profile_fixture("missingness-vertical-sampling-quarantine")
        before = deepcopy(fixture)
        ocean.ghc_family_validate_ocean_profile_surface(fixture)
        self.assertEqual(fixture, before)

    def test_runner_profiles_cover_each_surface_once(self) -> None:
        covered = [surface for values in ocean.RUNNER_PROFILES.values() for surface in values]
        self.assertEqual(len(ocean.RUNNER_PROFILES), 10)
        self.assertEqual(Counter(covered), Counter(ocean.SPEC_BY_SLUG.keys()))

    def test_unknown_profile_rejects(self) -> None:
        with self.assertRaises(ocean.EvidenceError):
            ocean.ghc_family_run_ocean_profile("unknown")

    def test_cli_single_profile_is_valid(self) -> None:
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "ghc_family_ocean_profile_evidence.py"), "--profile", "terminal-refusal"], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])


def surface_test(surface: str):
    def test(self: OceanProfileEvidenceTests) -> None:
        result = ocean.ghc_family_execute_ocean_profile_surface(surface)
        self.assertTrue(result["valid"])
        self.assertEqual((result["mutation_count"], result["rejected_mutation_count"]), (5, 5))
        self.assertFalse(result["post_success_replay"])
    return test


def runner_test(profile: str):
    def test(self: OceanProfileEvidenceTests) -> None:
        result = ocean.ghc_family_run_ocean_profile(profile)
        self.assertTrue(result["valid"])
        self.assertEqual((result["network_calls"], result["downloads"], result["profile_rows"]), (0, 0, 0))
    return test


for _surface in ocean.SPEC_BY_SLUG:
    setattr(OceanProfileEvidenceTests, f"test_surface_{_surface.replace('-', '_')}", surface_test(_surface))
for _profile in ocean.RUNNER_PROFILES:
    setattr(OceanProfileEvidenceTests, f"test_runner_{_profile.replace('-', '_')}", runner_test(_profile))


class FlashcardTests(unittest.TestCase):
    def model(self) -> dict:
        return flashcards.build_model(PHASE, X1)

    def test_dynamic_owner_phase_and_route(self) -> None:
        model = self.model()
        self.assertEqual((model["index"]["owner"], model["index"]["phase"]), ("Auren Lark", "v664-v6"))
        self.assertEqual(model["index"]["successor_route"], {"owner": "Sable Rook", "phase": "v664-v7", "contacted": False})

    def test_exact_tier_and_card_counts(self) -> None:
        model = self.model()
        self.assertEqual(model["index"]["expected_tier_counts"], {"1": 1, "2": 3, "3": 1, "4": 248})
        self.assertEqual(model["index"]["card_count"], 253)

    def test_four_core_outcomes(self) -> None:
        self.assertEqual(self.model()["index"]["new_core_outcomes"], {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4})

    def test_compact_pointer_is_unsent(self) -> None:
        text = flashcards.compact_message(self.model())
        self.assertIn("PREPARED_NOT_SENT = true", text)
        self.assertIn("SENT = false", text)
        self.assertEqual(flashcards.private_candidates(text), [])

    def test_accessible_report_has_structure(self) -> None:
        text = flashcards.accessible_report(self.model())
        self.assertIn("Auren Lark", text)
        self.assertIn('<main id="main">', text)
        self.assertIn("<caption>", text)

    def test_invalid_x1_rejects(self) -> None:
        with self.assertRaises(flashcards.FlashcardError):
            flashcards.build_model(PHASE, "not-an-object")

    def test_loaded_deck_validates(self) -> None:
        result = flashcards.validate_deck(ROOT, "docs/auren-lark/v664-v6/deck")
        self.assertTrue(result["valid"])
        self.assertEqual(result["model"]["card_count"], 253)

    def test_deck_manifest_replays(self) -> None:
        deck, _ = flashcards.load_deck(ROOT, "docs/auren-lark/v664-v6/deck")
        self.assertTrue(flashcards.manifest_status(deck)["valid"])

    def test_deck_privacy_is_clear(self) -> None:
        deck, _ = flashcards.load_deck(ROOT, "docs/auren-lark/v664-v6/deck")
        self.assertEqual(flashcards.privacy_status(deck)["candidate_count"], 0)

    def test_sixty_deck_mutations_reject(self) -> None:
        result = flashcards.mutation_receipt(ROOT, "docs/auren-lark/v664-v6/deck")
        self.assertEqual((result["mutation_count"], result["rejected_count"]), (60, 60))
        self.assertTrue(result["valid"])

    def test_wrong_output_directory_rejects(self) -> None:
        with self.assertRaises(flashcards.FlashcardError):
            flashcards.build_outputs(ROOT, "docs/auren-lark/v664-v6", "docs/auren-lark/v664-v6/not-deck", X1)

    def test_dangling_leaf_symlink_rejects_without_escape(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auren-link-regression-") as directory:
            root = Path(directory)
            inside, outside = root / "inside", root / "outside"
            inside.mkdir()
            outside.mkdir()
            target = outside / "escaped.bin"
            link = inside / "artifact.bin"
            link.symlink_to(target)
            with self.assertRaises(flashcards.FlashcardError):
                flashcards.write_equal_or_new(link, b"bounded")
            self.assertFalse(target.exists())


class MaterializedEvidenceTests(unittest.TestCase):
    def test_phase_truth_counts(self) -> None:
        truth = load("x2/phase-truth.json")
        self.assertEqual(truth["new_outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertTrue(truth["valid"])

    def test_negative_register_reconciles(self) -> None:
        record = load("x2/retained-negative-register.json")
        self.assertEqual(record["effective_negatives"], record["negatives_at_x1_freeze"] + len(record["new_records"]))
        self.assertEqual(record["x2_preregistered_synthetic_negatives"], 100)
        self.assertTrue(record["no_negative_erased"])

    def test_method_flow_reconciles(self) -> None:
        record = load("x2/method-flow-state.json")
        self.assertEqual(record["effective_methods"], record["methods_at_x1_freeze"] + len(record["methods"]))
        self.assertTrue(record["no_failure_erased"])

    def test_gate_register_remains_open(self) -> None:
        record = load("x2/open-gate-register.json")
        self.assertEqual((record["effective_open_gaps"], record["effective_exact_gates"]), (172, 170))
        self.assertEqual(record["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_surface_triplets_exist(self) -> None:
        for row in ocean.SURFACE_SPECS:
            base = PHASE / "x2" / "surfaces" / row["surface"]
            self.assertEqual({path.name for path in base.iterdir()}, {"contract.json", "mutation-results.json", "bounded-receipt.json"})

    def test_ten_local_skills_exist(self) -> None:
        rows = sorted((PHASE / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(rows), 10)
        self.assertTrue(all((path.parent / "smoke-receipt.json").is_file() for path in rows))

    def test_ten_runner_receipts_exist(self) -> None:
        self.assertEqual(len(list((PHASE / "x2" / "runners").glob("*.json"))), 10)

    def test_portfolio_counts_match(self) -> None:
        self.assertEqual(load("x2/portfolio-execution.json")["counts"], load("x1/portfolio-freeze.json")["counts"])

    def test_successor_is_not_contacted(self) -> None:
        record = load("x2/successor-recommendations.json")
        self.assertFalse(record["contacted"])
        self.assertEqual(record["execution_credit"], 0)

    def test_x1_immutability_receipt(self) -> None:
        record = load("x2/x1-immutability-receipt.json")
        self.assertEqual(record["x1"], X1)
        self.assertEqual(record["working_x1_changes"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
