#!/usr/bin/env python3
"""Bounded Ilyra v662-v6 tests for the exact modified owner-delta modules."""

from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_owner_delta_phase_builder as builder  # noqa: E402
import ghc_family_owner_delta_toolkit as toolkit  # noqa: E402


PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v662-v6"
X1 = PHASE_ROOT / "x1"
DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_owner_delta_phase_builder.py",
    "scripts/ghc_family_owner_delta_toolkit.py",
]


def load(name: str) -> dict:
    return toolkit.strict_json_loads((X1 / name).read_bytes(), name)


class ResourceBudgetTests(unittest.TestCase):
    def test_decompression_budget_passes_without_decoder(self) -> None:
        result = toolkit.validate_decompression_budget(10, 100, 100, 10)
        self.assertTrue(result["valid"])
        self.assertFalse(result["decoder_invoked"])

    def test_decompression_zero_compressed_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_decompression_budget(0, 0, 100, 10)

    def test_decompression_expanded_budget_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_decompression_budget(10, 101, 100, 20)

    def test_decompression_ratio_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_decompression_budget(10, 101, 1000, 10)

    def test_decompression_boolean_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_decompression_budget(True, 1, 10, 10)

    def test_sparse_size_distinguishes_fields(self) -> None:
        result = toolkit.sparse_size_record(1000, 10)
        self.assertTrue(result["sparse"])
        self.assertFalse(result["file_materialized"])

    def test_sparse_equal_size_not_sparse(self) -> None:
        self.assertFalse(toolkit.sparse_size_record(10, 10)["sparse"])

    def test_sparse_stored_over_logical_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.sparse_size_record(10, 11)

    def test_sparse_negative_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.sparse_size_record(-1, 0)

    def test_sparse_boolean_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.sparse_size_record(True, 0)


class PathAndUriTests(unittest.TestCase):
    def test_regular_archive_entry_passes(self) -> None:
        self.assertEqual(toolkit.validate_archive_entry_kind("regular_file"), "regular_file")

    def test_directory_archive_entry_passes(self) -> None:
        self.assertEqual(toolkit.validate_archive_entry_kind("directory"), "directory")

    def test_symlink_entry_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_archive_entry_kind("symlink")

    def test_hardlink_entry_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_archive_entry_kind("hardlink")

    def test_unknown_entry_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_archive_entry_kind("socket")

    def test_relative_windows_reference_passes(self) -> None:
        self.assertEqual(toolkit.validate_windows_archive_reference("safe/a.txt"), "safe/a.txt")

    def test_unc_reference_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_windows_archive_reference(r"\\server\share\a.txt")

    def test_extended_reference_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_windows_archive_reference(r"\\?\C:\a.txt")

    def test_drive_reference_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_windows_archive_reference(r"C:\a.txt")

    def test_uri_unreserved_percent_normalizes(self) -> None:
        self.assertEqual(toolkit.normalize_uri_member_reference("safe/%7eitem.txt"), "safe/~item.txt")

    def test_uri_reserved_percent_remains_encoded(self) -> None:
        self.assertEqual(toolkit.normalize_uri_member_reference("safe/a%2fb.txt"), "safe/a%2Fb.txt")

    def test_uri_malformed_percent_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_uri_member_reference("safe/%2.txt")

    def test_uri_encoded_parent_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_uri_member_reference("safe/%2e%2e/escape.txt")

    def test_uri_scheme_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_uri_member_reference("https://example.invalid/a.txt")

    def test_uri_query_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_uri_member_reference("safe/a.txt?version=1")


class NumericAndMediaTests(unittest.TestCase):
    def test_json_number_integer_passes(self) -> None:
        self.assertEqual(toolkit.validate_json_number_lexeme("0"), "0")

    def test_json_number_fraction_exponent_passes(self) -> None:
        self.assertEqual(toolkit.validate_json_number_lexeme("-1.25e+3"), "-1.25e+3")

    def test_json_number_leading_plus_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_number_lexeme("+1")

    def test_json_number_leading_zero_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_number_lexeme("01")

    def test_json_number_empty_fraction_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_number_lexeme("1.")

    def test_json_number_exponent_budget_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_number_lexeme("1e309")

    def test_json_number_character_budget_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_number_lexeme("1" * 65)

    def test_finite_number_passes(self) -> None:
        self.assertEqual(toolkit.validate_schema_finite_number(1.25), 1.25)

    def test_nan_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_schema_finite_number(math.nan)

    def test_infinity_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_schema_finite_number(math.inf)

    def test_negative_zero_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_schema_finite_number(-0.0)

    def test_boolean_number_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_schema_finite_number(True)

    def test_declared_media_type_passes(self) -> None:
        self.assertEqual(toolkit.validate_media_type("APPLICATION/VND.IN-TOTO+JSON"), "application/vnd.in-toto+json")

    def test_unknown_media_type_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_media_type("application/octet-stream")

    def test_parameterized_media_type_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_media_type("application/vnd.in-toto+json; charset=utf-8")


class AttestationTests(unittest.TestCase):
    def subject(self) -> dict:
        return {"name": "object.json", "digest": {"sha256": "00" * 32}}

    def test_subject_digest_agrees_without_provenance(self) -> None:
        result = toolkit.validate_subject_digest_agreement([self.subject()])
        self.assertTrue(result["valid"])
        self.assertFalse(result["provenance_verified"])

    def test_subject_digest_wrong_algorithm_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_subject_digest_agreement(
                [{"name": "object.json", "digest": {"sha512": "00" * 64}}]
            )

    def test_subject_digest_wrong_width_refused(self) -> None:
        row = self.subject()
        row["digest"]["sha256"] = "00"
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_subject_digest_agreement([row])

    def test_subject_digest_uppercase_refused(self) -> None:
        row = self.subject()
        row["digest"]["sha256"] = "AA" * 32
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_subject_digest_agreement([row])

    def test_duplicate_subject_name_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_subject_digest_agreement([self.subject(), self.subject()])

    def test_dsse_pae_official_shape_vector(self) -> None:
        self.assertEqual(
            toolkit.dsse_pae("http://example.com/HelloWorld", b"hello world"),
            b"DSSEv1 29 http://example.com/HelloWorld 11 hello world",
        )

    def test_dsse_pae_payload_mutation_changes_bytes(self) -> None:
        first = toolkit.dsse_pae("application/vnd.in-toto+json", b"A")
        second = toolkit.dsse_pae("application/vnd.in-toto+json", b"B")
        self.assertNotEqual(first, second)

    def test_dsse_pae_non_ascii_type_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.dsse_pae("application/vnd.ghc.mānuka", b"payload")

    def test_declared_predicate_passes(self) -> None:
        value = "https://example.invalid/ghc/synthetic-condition/v1"
        self.assertEqual(toolkit.validate_predicate_type(value), value)

    def test_unknown_predicate_version_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_predicate_type("https://example.invalid/ghc/synthetic-condition/v2")

    def test_non_https_predicate_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_predicate_type("http://example.invalid/ghc/synthetic-condition/v1")


class TimeAndPointerTests(unittest.TestCase):
    def test_clock_rollback_flagged(self) -> None:
        result = toolkit.clock_separation_record(10, 9, 1)
        self.assertTrue(result["wall_clock_rollback_detected"])
        self.assertFalse(result["trusted_time"])

    def test_clock_forward_not_rollback(self) -> None:
        self.assertFalse(toolkit.clock_separation_record(9, 10, 1)["wall_clock_rollback_detected"])

    def test_negative_monotonic_duration_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.clock_separation_record(10, 9, -1)

    def test_rfc3339_z_passes(self) -> None:
        self.assertEqual(toolkit.normalize_rfc3339_utc("2026-08-18T10:00:00Z"), "2026-08-18T10:00:00Z")

    def test_rfc3339_offset_normalizes(self) -> None:
        self.assertEqual(toolkit.normalize_rfc3339_utc("2026-08-18T22:00:00+12:00"), "2026-08-18T10:00:00Z")

    def test_rfc3339_fraction_preserved(self) -> None:
        self.assertEqual(toolkit.normalize_rfc3339_utc("2026-08-18T10:00:00.500Z"), "2026-08-18T10:00:00.500000Z")

    def test_rfc3339_naive_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_rfc3339_utc("2026-08-18T10:00:00")

    def test_rfc3339_unknown_offset_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_rfc3339_utc("2026-08-18T10:00:00-00:00")

    def test_json_pointer_canonical_escape(self) -> None:
        self.assertEqual(toolkit.normalize_json_pointer("/a~1b/~0c"), "/a~1b/~0c")

    def test_json_pointer_invalid_escape_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_json_pointer("/a~2b")

    def test_json_pointer_nonabsolute_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_json_pointer("a/b")

    def test_unique_json_pointer_targets_pass(self) -> None:
        self.assertEqual(
            toolkit.validate_unique_json_pointer_targets(["/condition", "/custody/state"]),
            ["/condition", "/custody/state"],
        )

    def test_duplicate_json_pointer_targets_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_unique_json_pointer_targets(["/a~1b", "/a~1b"])


class HardeningAndProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = load("builder-profile.json")
        cls.proposals = load("proposal-freeze.json")
        cls.portfolio = load("portfolio-freeze.json")
        cls.startup = load("startup-method-flow.json")
        cls.runtime = toolkit.strict_json_loads(
            (PHASE_ROOT / "x2" / "operational-method-flow.json").read_bytes(),
            "operational-method-flow.json",
        )

    def test_hardening_payload_counts(self) -> None:
        result = toolkit.hardening_payload()
        self.assertEqual(result["negative_fixture_count"], 14)
        self.assertEqual(result["rejected_fixture_count"], 14)
        self.assertEqual(result["positive_fixture_count"], 14)
        self.assertEqual(result["passing_fixture_count"], 14)
        self.assertFalse(result["signature_verified"])
        self.assertFalse(result["provenance_verified"])

    def test_phase_root_confinement(self) -> None:
        self.assertEqual(
            builder.confined_phase_root(ROOT, "docs/ilyra-fen/v662-v6", "Ilyra Fen", "v662-v6"),
            PHASE_ROOT.resolve(),
        )

    def test_phase_root_wrong_owner_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            builder.confined_phase_root(ROOT, "docs/other/v662-v6", "Ilyra Fen", "v662-v6")

    def test_profile_child_escape_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            builder.confined_profile_child(PHASE_ROOT, "../../escape.txt")

    def test_profile_ledgers_match_frozen_counts(self) -> None:
        ledgers = builder.build_profile_ledgers(self.portfolio, "Ilyra Fen", "v662-v6")
        self.assertEqual(ledgers["safe-now-ledger"]["record_count"], 50)
        self.assertEqual(ledgers["candidate-ledger"]["record_count"], 30)
        self.assertEqual(ledgers["approval-gate-ledger"]["record_count"], 15)
        self.assertEqual(ledgers["skill-ledger"]["record_count"], 20)
        self.assertEqual(ledgers["runner-ledger"]["record_count"], 20)
        self.assertEqual(ledgers["clean-fix-refine-ledger"]["record_count"], 60)

    def test_profile_method_flow_retains_every_record(self) -> None:
        methods, hardening = builder.profile_method_flow(
            self.startup, self.runtime, "Ilyra Fen", "v662-v6"
        )
        self.assertEqual(methods["method_count"], 26)
        self.assertEqual(methods["retained_failed_witness_count"], 26)
        self.assertEqual(hardening["rejected_fixture_count"], 14)

    def test_profile_sources_are_primary_or_official(self) -> None:
        sources = builder.profile_source_ledger("Ilyra Fen", "v662-v6")
        self.assertEqual(sources["record_count"], 18)
        self.assertTrue(all(record["url"].startswith("https://") for record in sources["records"]))

    def test_profile_baton_is_in_word_contract(self) -> None:
        ledgers = builder.build_profile_ledgers(self.portfolio, "Ilyra Fen", "v662-v6")
        methods, _ = builder.profile_method_flow(
            self.startup, self.runtime, "Ilyra Fen", "v662-v6"
        )
        text = builder.profile_baton_text(
            "Ilyra Fen",
            "Auren Lark",
            "v662-v6",
            "v662-v7",
            "792d58170cf7badae2a233dc39bccb6fd653edb7",
            "bb8a93e6ed483ecf23ea2c0d81e4d821ac5f0a32",
            self.profile,
            self.proposals["new_proposals"],
            ledgers,
            methods,
        )
        count = builder.words(text)
        self.assertGreaterEqual(count, 10000)
        self.assertLessEqual(count, 100000)
        self.assertIn("Auren Lark v662-v7 activation baton", text)
        self.assertNotIn("source_thread_id", text)

    def test_static_report_has_structural_regions(self) -> None:
        outcome = {"outcome_counts": self.profile["outcome_counts"]}
        report = builder.profile_static_report(
            "Ilyra Fen", "v662-v6", "bounded overview", outcome
        )
        self.assertIn("<main>", report)
        self.assertIn("<table>", report)
        self.assertIn("<caption>", report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)

    def test_x1_profile_matches_frozen_proposal_total(self) -> None:
        self.assertEqual(self.profile["proposal_total"], 3630)
        self.assertEqual(self.proposals["new_frozen_total"], 3630)
        self.assertEqual(len(self.proposals["new_proposals"]), 20)

    def test_runner_contract_test_path_is_profile_derived(self) -> None:
        self.assertEqual(self.profile["test_modules"], ["tests/test_ghc_family_ilyra_v662_v6.py"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
