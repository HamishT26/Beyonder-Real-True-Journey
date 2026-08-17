#!/usr/bin/env python3
"""Bounded Lyren v662-v5 tests for the exact modified owner-delta modules."""

from __future__ import annotations

import base64
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_owner_delta_phase_builder as builder  # noqa: E402
import ghc_family_owner_delta_toolkit as toolkit  # noqa: E402


PHASE_ROOT = ROOT / "docs" / "lyren-moss" / "v662-v5"
X1 = PHASE_ROOT / "x1"
DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_owner_delta_phase_builder.py",
    "scripts/ghc_family_owner_delta_toolkit.py",
]


def load(name: str) -> dict:
    return toolkit.strict_json_loads((X1 / name).read_bytes(), name)


def valid_dsse() -> dict:
    return {
        "payloadType": "application/vnd.example.synthetic",
        "payload": base64.b64encode(b"payload").decode("ascii"),
        "signatures": [
            {
                "keyid": "synthetic-key",
                "sig": base64.b64encode(b"signature-shape-only").decode("ascii"),
            }
        ],
    }


def valid_statement() -> dict:
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {"name": "synthetic.bin", "digest": {"sha256": "00" * 32}}
        ],
        "predicateType": "https://example.invalid/predicate/synthetic/v1",
        "predicate": {"synthetic": True},
    }


class PathAndArchiveTests(unittest.TestCase):
    def test_windows_component_safe(self) -> None:
        self.assertEqual(toolkit.validate_windows_component("report.v1"), "report.v1")

    def test_windows_reserved_device_refused(self) -> None:
        for value in ("CON", "aux.txt", "Lpt9.log", "NUL"):
            with self.subTest(value=value), self.assertRaises(toolkit.DeltaError):
                toolkit.validate_windows_component(value)

    def test_windows_trailing_dot_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_windows_component("report.")

    def test_windows_trailing_space_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_windows_component("report ")

    def test_windows_separator_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_windows_component("a/b")

    def test_archive_member_safe_normalization(self) -> None:
        self.assertEqual(
            toolkit.normalize_archive_member("a/./b//c.txt"), "a/b/c.txt"
        )

    def test_archive_parent_traversal_slash_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_archive_member("a/../b.txt")

    def test_archive_parent_traversal_backslash_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_archive_member("a\\..\\b.txt")

    def test_archive_absolute_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_archive_member("/absolute.txt")

    def test_archive_drive_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_archive_member("C:\\escape.txt")

    def test_archive_reserved_component_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_archive_member("safe/CON.txt")

    def test_unique_archive_members(self) -> None:
        self.assertEqual(
            toolkit.normalize_unique_archive_members(["a.txt", "b/./c.txt"]),
            ["a.txt", "b/c.txt"],
        )

    def test_duplicate_normalized_archive_members_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_unique_archive_members(["a/./b.txt", "a/b.txt"])


class ConfusableAndAttestationTests(unittest.TestCase):
    def test_bounded_confusable_match(self) -> None:
        self.assertEqual(
            toolkit.bounded_confusable_skeleton("PΑYLOAD"),
            toolkit.bounded_confusable_skeleton("PAYLOAD"),
        )

    def test_bounded_confusable_ordinary(self) -> None:
        self.assertEqual(toolkit.bounded_confusable_skeleton("Ordinary"), "ordinary")

    def test_dsse_valid_shape_does_not_verify_signature(self) -> None:
        result = toolkit.validate_dsse_envelope(valid_dsse())
        self.assertTrue(result["valid"])
        self.assertFalse(result["signature_verified"])

    def test_dsse_malformed_payload_refused(self) -> None:
        envelope = valid_dsse()
        envelope["payload"] = "%%%"
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_dsse_envelope(envelope)

    def test_dsse_duplicate_key_identifier_refused(self) -> None:
        envelope = valid_dsse()
        envelope["signatures"].append(dict(envelope["signatures"][0]))
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_dsse_envelope(envelope)

    def test_dsse_empty_signatures_refused(self) -> None:
        envelope = valid_dsse()
        envelope["signatures"] = []
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_dsse_envelope(envelope)

    def test_intoto_valid_shape_does_not_verify_provenance(self) -> None:
        result = toolkit.validate_intoto_statement(valid_statement())
        self.assertTrue(result["valid"])
        self.assertFalse(result["provenance_verified"])

    def test_intoto_wrong_type_refused(self) -> None:
        statement = valid_statement()
        statement["_type"] = "wrong"
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_intoto_statement(statement)

    def test_intoto_missing_digest_refused(self) -> None:
        statement = valid_statement()
        statement["subject"] = [{"name": "synthetic.bin"}]
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_intoto_statement(statement)

    def test_intoto_nonhex_digest_refused(self) -> None:
        statement = valid_statement()
        statement["subject"][0]["digest"]["sha256"] = "not-hex"
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_intoto_statement(statement)

    def test_intoto_duplicate_subject_refused(self) -> None:
        statement = valid_statement()
        statement["subject"].append(dict(statement["subject"][0]))
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_intoto_statement(statement)


class DeterminismAndModeTests(unittest.TestCase):
    def test_declared_clock_sources(self) -> None:
        for value in toolkit.DECLARED_CLOCK_SOURCES:
            with self.subTest(value=value):
                self.assertEqual(toolkit.validate_clock_source(value), value)

    def test_unknown_clock_source_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_clock_source("ambient")

    def test_option_like_clock_source_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_clock_source("--help")

    def test_locale_invariant_order(self) -> None:
        expected = ["A", "z", "ä"]
        self.assertEqual(toolkit.locale_invariant_order(["ä", "A", "z"]), expected)
        self.assertEqual(toolkit.locale_invariant_order(["z", "ä", "A"]), expected)

    def test_semantic_commitment_ignores_observation_time(self) -> None:
        first = toolkit.semantic_content_sha256(
            {"value": 1, "observed_at_utc": "A"}
        )
        second = toolkit.semantic_content_sha256(
            {"value": 1, "observed_at_utc": "B"}
        )
        self.assertEqual(first, second)

    def test_semantic_commitment_changes_with_content(self) -> None:
        first = toolkit.semantic_content_sha256({"value": 1})
        second = toolkit.semantic_content_sha256({"value": 2})
        self.assertNotEqual(first, second)

    def test_executable_mode_allowlist_passes(self) -> None:
        result = toolkit.validate_executable_modes(
            [{"path": "bin/tool.py", "mode": "100755"}], ["bin/tool.py"]
        )
        self.assertTrue(result["valid"])

    def test_unallowlisted_executable_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_executable_modes(
                [{"path": "bin/tool.py", "mode": "100755"}], []
            )

    def test_allowlisted_nonexecutable_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_executable_modes(
                [{"path": "bin/tool.py", "mode": "100644"}], ["bin/tool.py"]
            )

    def test_utf8_strict_accepts_valid_text(self) -> None:
        self.assertEqual(
            toolkit.decode_utf8_strict("mānuka".encode("utf-8")), "mānuka"
        )

    def test_utf8_strict_refuses_malformed_bytes(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.decode_utf8_strict(b"\xff\xfe")

    def test_digest_algorithm_normalizes_sha256(self) -> None:
        self.assertEqual(toolkit.validate_digest_algorithm(" SHA256 "), "sha256")

    def test_unknown_digest_algorithm_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_digest_algorithm("sha1")

    def test_option_like_digest_algorithm_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_digest_algorithm("--help")


class FramingAndAggregateTests(unittest.TestCase):
    def leaf(self) -> dict:
        return {
            "path": "a/b.txt",
            "mode": "100644",
            "git_blob": "0" * 40,
            "bytes": 3,
            "sha256": "0" * 64,
        }

    def test_leaf_framing_is_deterministic(self) -> None:
        leaf = self.leaf()
        self.assertEqual(toolkit.frame_merkle_leaf(leaf), toolkit.frame_merkle_leaf(dict(leaf)))

    def test_leaf_framing_distinguishes_fields(self) -> None:
        first = self.leaf()
        second = dict(first, path="a", mode="b.txt100644")
        self.assertNotEqual(toolkit.frame_merkle_leaf(first), toolkit.frame_merkle_leaf(second))

    def test_leaf_framing_requires_all_fields(self) -> None:
        leaf = self.leaf()
        del leaf["sha256"]
        with self.assertRaises(toolkit.DeltaError):
            toolkit.frame_merkle_leaf(leaf)

    def test_hardening_payload_counts(self) -> None:
        result = toolkit.hardening_payload()
        self.assertEqual(result["negative_fixture_count"], 14)
        self.assertEqual(result["rejected_fixture_count"], 14)
        self.assertEqual(result["positive_fixture_count"], 14)
        self.assertEqual(result["passing_fixture_count"], 14)
        self.assertFalse(result["signature_verified"])
        self.assertFalse(result["provenance_verified"])


class ProfileBuilderTests(unittest.TestCase):
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

    def test_phase_root_confinement(self) -> None:
        self.assertEqual(
            builder.confined_phase_root(ROOT, "docs/lyren-moss/v662-v5", "Lyren Moss", "v662-v5"),
            PHASE_ROOT.resolve(),
        )

    def test_phase_root_wrong_owner_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            builder.confined_phase_root(ROOT, "docs/other/v662-v5", "Lyren Moss", "v662-v5")

    def test_profile_child_escape_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            builder.confined_profile_child(PHASE_ROOT, "../../escape.txt")

    def test_profile_ledgers_match_frozen_counts(self) -> None:
        ledgers = builder.build_profile_ledgers(self.portfolio, "Lyren Moss", "v662-v5")
        self.assertEqual(ledgers["safe-now-ledger"]["record_count"], 50)
        self.assertEqual(ledgers["candidate-ledger"]["record_count"], 30)
        self.assertEqual(ledgers["approval-gate-ledger"]["record_count"], 15)
        self.assertEqual(ledgers["skill-ledger"]["record_count"], 20)
        self.assertEqual(ledgers["runner-ledger"]["record_count"], 20)
        self.assertEqual(ledgers["clean-fix-refine-ledger"]["record_count"], 60)

    def test_profile_method_flow_retains_every_record(self) -> None:
        methods, hardening = builder.profile_method_flow(
            self.startup, self.runtime, "Lyren Moss", "v662-v5"
        )
        self.assertEqual(methods["method_count"], 28)
        self.assertEqual(methods["retained_failed_witness_count"], 28)
        self.assertEqual(hardening["rejected_fixture_count"], 14)

    def test_profile_sources_are_primary_or_official(self) -> None:
        sources = builder.profile_source_ledger("Lyren Moss", "v662-v5")
        self.assertEqual(sources["record_count"], 12)
        self.assertTrue(all(record["url"].startswith("https://") for record in sources["records"]))

    def test_profile_baton_is_in_word_contract(self) -> None:
        ledgers = builder.build_profile_ledgers(self.portfolio, "Lyren Moss", "v662-v5")
        methods, _ = builder.profile_method_flow(
            self.startup, self.runtime, "Lyren Moss", "v662-v5"
        )
        text = builder.profile_baton_text(
            "Lyren Moss",
            "Ilyra Fen",
            "v662-v5",
            "v662-v6",
            "1605c722d40be5c75c669ed96551f2fc6c208d67",
            "36315f6aee6aea9465927a42decd95d62a328117",
            self.profile,
            self.proposals["new_proposals"],
            ledgers,
            methods,
        )
        count = builder.words(text)
        self.assertGreaterEqual(count, 10000)
        self.assertLessEqual(count, 100000)
        self.assertIn("Ilyra Fen v662-v6 activation baton", text)
        self.assertNotIn("source_thread_id", text)

    def test_static_report_has_structural_regions(self) -> None:
        outcome = {"outcome_counts": self.profile["outcome_counts"]}
        report = builder.profile_static_report(
            "Lyren Moss", "v662-v5", "bounded overview", outcome
        )
        self.assertIn("<main>", report)
        self.assertIn("<table>", report)
        self.assertIn("<caption>", report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)

    def test_x1_profile_matches_frozen_proposal_total(self) -> None:
        self.assertEqual(self.profile["proposal_total"], 3610)
        self.assertEqual(self.proposals["new_frozen_total"], 3610)
        self.assertEqual(len(self.proposals["new_proposals"]), 20)


if __name__ == "__main__":
    unittest.main(verbosity=2)
