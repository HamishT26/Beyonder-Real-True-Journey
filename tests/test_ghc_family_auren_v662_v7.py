#!/usr/bin/env python3
"""Bounded Auren v662-v7 tests for the exact modified owner-delta modules."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_owner_delta_phase_builder as builder  # noqa: E402
import ghc_family_owner_delta_toolkit as toolkit  # noqa: E402


PHASE_ROOT = ROOT / "docs" / "auren-lark" / "v662-v7"
X1 = PHASE_ROOT / "x1"
DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_owner_delta_phase_builder.py",
    "scripts/ghc_family_owner_delta_toolkit.py",
]


def load(name: str) -> dict:
    return toolkit.strict_json_loads((X1 / name).read_bytes(), name)


class ByteOrderAndPermissionTests(unittest.TestCase):
    def test_little_byte_order_passes(self) -> None:
        self.assertEqual(toolkit.validate_byte_order("little"), "little")

    def test_big_byte_order_passes(self) -> None:
        self.assertEqual(toolkit.validate_byte_order("big"), "big")

    def test_network_byte_order_passes(self) -> None:
        self.assertEqual(toolkit.validate_byte_order("network"), "network")

    def test_native_byte_order_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_byte_order("native")

    def test_padded_byte_order_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_byte_order(" big ")

    def test_permission_mode_passes_without_filesystem(self) -> None:
        result = toolkit.normalize_permission_mode(0o640)
        self.assertEqual(result["octal"], "0640")
        self.assertFalse(result["filesystem_mutated"])

    def test_permission_mode_outside_mask_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_permission_mode(0o1000, 0o777)

    def test_permission_boolean_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_permission_mode(True)

    def test_permission_negative_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_permission_mode(-1)

    def test_permission_mask_over_budget_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_permission_mode(0, 0o17777)


class ResourceAndProductTests(unittest.TestCase):
    def nodes(self) -> list[dict]:
        return [
            {"depth": 1, "declared_bytes": 10},
            {"depth": 2, "declared_bytes": 20},
        ]

    def test_nested_budget_passes_without_allocation(self) -> None:
        result = toolkit.validate_nested_resource_budget(self.nodes(), 2, 2, 30)
        self.assertEqual(result["total_declared_bytes"], 30)
        self.assertFalse(result["resources_allocated"])

    def test_nested_budget_empty_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_nested_resource_budget([], 2, 2, 30)

    def test_nested_budget_member_count_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_nested_resource_budget(self.nodes(), 2, 1, 30)

    def test_nested_budget_depth_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_nested_resource_budget(
                [{"depth": 3, "declared_bytes": 1}], 2, 1, 30
            )

    def test_nested_budget_total_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_nested_resource_budget(self.nodes(), 2, 2, 29)

    def test_nested_budget_boolean_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_nested_resource_budget(
                [{"depth": 1, "declared_bytes": True}], 1, 1, 1
            )

    def test_checked_product_passes_at_ceiling(self) -> None:
        self.assertEqual(toolkit.checked_size_product(6, 7, 42), 42)

    def test_checked_product_zero_passes(self) -> None:
        self.assertEqual(toolkit.checked_size_product(0, 999, 0), 0)

    def test_checked_product_over_ceiling_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.checked_size_product(11, 10, 100)

    def test_checked_product_boolean_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.checked_size_product(True, 1, 1)

    def test_checked_product_negative_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.checked_size_product(-1, 1, 1)


class UriAndMediaTests(unittest.TestCase):
    def test_uri_relative_member_passes(self) -> None:
        self.assertEqual(
            toolkit.validate_uri_member_components("safe/item.json"),
            "safe/item.json",
        )

    def test_uri_unreserved_octet_normalizes(self) -> None:
        self.assertEqual(
            toolkit.validate_uri_member_components("safe/%7eitem.json"),
            "safe/~item.json",
        )

    def test_uri_query_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_uri_member_components("safe/item.json?revision=1")

    def test_uri_empty_query_delimiter_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_uri_member_components("safe/item.json?")

    def test_uri_fragment_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_uri_member_components("safe/item.json#part")

    def test_uri_scheme_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_uri_member_components("https://example.invalid/item")

    def test_uri_encoded_slash_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_uri_member_components("safe/a%2fb.json")

    def test_uri_encoded_backslash_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_uri_member_components("safe/a%5cb.json")

    def test_uri_encoded_parent_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_uri_member_components("safe/%2e%2e/item.json")

    def test_media_parameters_pass_without_content(self) -> None:
        result = toolkit.parse_media_type_parameters(
            "APPLICATION/VND.IN-TOTO+JSON; charset=UTF-8; version=1"
        )
        self.assertEqual(result["parameters"], {"charset": "utf-8", "version": "1"})
        self.assertFalse(result["content_opened"])

    def test_media_duplicate_parameter_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.parse_media_type_parameters(
                "application/vnd.in-toto+json; charset=utf-8; CHARSET=utf-8"
            )

    def test_media_unknown_charset_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.parse_media_type_parameters(
                "application/vnd.in-toto+json; charset=iso-8859-1"
            )

    def test_media_unknown_parameter_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.parse_media_type_parameters(
                "application/vnd.in-toto+json; boundary=abc"
            )

    def test_media_parameter_count_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.parse_media_type_parameters(
                "application/vnd.in-toto+json; charset=utf-8; profile=a; version=1; profile=b; version=2"
            )

    def test_media_quoted_parameter_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.parse_media_type_parameters(
                'application/vnd.in-toto+json; charset="utf-8"'
            )


class AttestationBoundaryTests(unittest.TestCase):
    def test_digest_policy_sha256_passes_without_crypto(self) -> None:
        result = toolkit.validate_digest_policy({"sha256": "00" * 32})
        self.assertFalse(result["cryptographic_validity_verified"])
        self.assertFalse(result["provenance_verified"])

    def test_digest_policy_sha256_and_sha512_pass(self) -> None:
        result = toolkit.validate_digest_policy(
            {"sha256": "00" * 32, "sha512": "11" * 64}
        )
        self.assertEqual(result["algorithms"], ["sha256", "sha512"])

    def test_digest_policy_reserved_algorithm_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_digest_policy({"sha1": "00" * 20})

    def test_digest_policy_uppercase_label_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_digest_policy({"SHA256": "00" * 32})

    def test_digest_policy_wrong_width_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_digest_policy({"sha256": "00"})

    def test_digest_policy_required_algorithm_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_digest_policy({"sha512": "00" * 64})

    def test_dsse_payload_type_passes(self) -> None:
        self.assertEqual(
            toolkit.validate_dsse_payload_type("application/vnd.in-toto+json"),
            "application/vnd.in-toto+json",
        )

    def test_dsse_payload_type_unicode_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_dsse_payload_type("application/vnd.ghc.mānuka")

    def test_dsse_payload_type_whitespace_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_dsse_payload_type("application/json value")

    def test_dsse_payload_type_length_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_dsse_payload_type("abcd", maximum_bytes=3)

    def test_subject_names_pass_without_identity(self) -> None:
        self.assertEqual(
            toolkit.validate_unique_attestation_subject_names(["Object-A", "Object-B"]),
            ["Object-A", "Object-B"],
        )

    def test_subject_names_case_collision_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_unique_attestation_subject_names(["Object", "object"])

    def test_subject_names_nfc_collision_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_unique_attestation_subject_names(["é", "e\u0301"])

    def test_subject_names_control_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_unique_attestation_subject_names(["object\u0000"])


class TimeAndPointerBoundaryTests(unittest.TestCase):
    def test_ordinary_timestamp_passes_without_trusted_time(self) -> None:
        result = toolkit.validate_rfc3339_leap_second_reservation(
            "2026-08-18T10:00:00Z"
        )
        self.assertFalse(result["reserved_leap_second"])
        self.assertFalse(result["trusted_time"])

    def test_leap_second_refused_by_default(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_rfc3339_leap_second_reservation(
                "2016-12-31T23:59:60Z"
            )

    def test_leap_second_can_be_returned_as_reserved(self) -> None:
        result = toolkit.validate_rfc3339_leap_second_reservation(
            "2016-12-31T23:59:60Z", allow_reserved_leap_second=True
        )
        self.assertTrue(result["reserved_leap_second"])
        self.assertFalse(result["trusted_time"])

    def test_second_over_sixty_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_rfc3339_leap_second_reservation(
                "2016-12-31T23:59:61Z"
            )

    def test_unknown_offset_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_rfc3339_leap_second_reservation(
                "2026-08-18T10:00:00-00:00"
            )

    def test_json_pointer_zero_index_passes(self) -> None:
        self.assertEqual(toolkit.validate_json_pointer_array_index("0"), 0)

    def test_json_pointer_positive_index_passes(self) -> None:
        self.assertEqual(toolkit.validate_json_pointer_array_index("10"), 10)

    def test_json_pointer_leading_zero_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_pointer_array_index("01")

    def test_json_pointer_dash_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_pointer_array_index("-")

    def test_json_pointer_over_maximum_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_json_pointer_array_index("11", maximum_index=10)


class RevisionGlossaryAndCustodyTests(unittest.TestCase):
    def report(self) -> dict:
        return {
            "record_ids": ["object-001", "object-002"],
            "schema_revision": "condition-v1",
            "content_revision": "7",
        }

    def glossary(self) -> dict:
        return {
            "glossary_id": "condition-v1",
            "revision": "7",
            "terms": ["stable", "surface_change"],
        }

    def test_revision_pair_passes_without_accessibility_claim(self) -> None:
        result = toolkit.validate_revision_pair(self.report(), self.report())
        self.assertEqual(result["record_count"], 2)
        self.assertFalse(result["accessibility_complete"])

    def test_revision_pair_record_order_is_set_like(self) -> None:
        alternative = self.report()
        alternative["record_ids"] = list(reversed(alternative["record_ids"]))
        self.assertTrue(toolkit.validate_revision_pair(self.report(), alternative)["valid"])

    def test_revision_pair_content_mismatch_refused(self) -> None:
        alternative = self.report()
        alternative["content_revision"] = "8"
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_revision_pair(self.report(), alternative)

    def test_revision_pair_wrong_fields_refused(self) -> None:
        alternative = self.report()
        alternative["extra"] = True
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_revision_pair(self.report(), alternative)

    def test_revision_pair_duplicate_record_refused(self) -> None:
        alternative = self.report()
        alternative["record_ids"] = ["object-001", "object-001"]
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_revision_pair(self.report(), alternative)

    def test_glossary_term_passes_without_authority(self) -> None:
        result = toolkit.validate_condition_term_revision(
            "stable", "condition-v1", "7", self.glossary()
        )
        self.assertFalse(result["professional_authority"])
        self.assertFalse(result["cultural_authority"])

    def test_glossary_revision_mismatch_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_condition_term_revision(
                "stable", "condition-v1", "8", self.glossary()
            )

    def test_glossary_missing_term_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_condition_term_revision(
                "crack", "condition-v1", "7", self.glossary()
            )

    def test_glossary_collision_refused(self) -> None:
        glossary = self.glossary()
        glossary["terms"] = ["Stable", "stable"]
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_condition_term_revision(
                "stable", "condition-v1", "7", glossary
            )

    def test_custody_transition_passes_without_authority(self) -> None:
        result = toolkit.validate_custody_transition(
            "storage", "review", 2, 2, False, "registrar-a", "registrar-b"
        )
        self.assertEqual(result["next_revision"], 3)
        self.assertFalse(result["custody_authority"])

    def test_custody_active_hold_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_custody_transition(
                "storage", "review", 2, 2, True, "registrar-a", "registrar-b"
            )

    def test_custody_stale_revision_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_custody_transition(
                "storage", "review", 1, 2, False, "registrar-a", "registrar-b"
            )

    def test_custody_undeclared_edge_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_custody_transition(
                "storage", "handover", 2, 2, False, "registrar-a", "registrar-b"
            )

    def test_custody_same_actor_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_custody_transition(
                "storage", "review", 2, 2, False, "registrar-a", "REGISTRAR-A"
            )

    def test_custody_nonboolean_hold_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.validate_custody_transition(
                "storage", "review", 2, 2, 0, "registrar-a", "registrar-b"
            )


class HardeningAndProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = load("builder-profile.json")
        cls.proposals = load("proposal-freeze.json")
        cls.portfolio = load("portfolio-freeze.json")
        cls.startup = load("startup-method-flow.json")

    def test_auren_hardening_payload_counts(self) -> None:
        result = toolkit.auren_hardening_payload()
        self.assertEqual(result["negative_fixture_count"], 14)
        self.assertEqual(result["rejected_fixture_count"], 14)
        self.assertEqual(result["positive_fixture_count"], 14)
        self.assertEqual(result["passing_fixture_count"], 14)
        self.assertFalse(result["signature_verified"])
        self.assertFalse(result["provenance_verified"])

    def test_legacy_hardening_dispatch_remains_available(self) -> None:
        result = toolkit.hardening_payload_for_profile("ilyra-v662-v6")
        self.assertEqual(result["rejected_fixture_count"], 14)

    def test_unknown_hardening_profile_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.hardening_payload_for_profile("unknown")

    def test_phase_root_confinement(self) -> None:
        self.assertEqual(
            builder.confined_phase_root(
                ROOT, "docs/auren-lark/v662-v7", "Auren Lark", "v662-v7"
            ),
            PHASE_ROOT.resolve(),
        )

    def test_profile_child_escape_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            builder.confined_profile_child(PHASE_ROOT, "../../escape.txt")

    def test_profile_ledgers_match_frozen_counts(self) -> None:
        ledgers = builder.build_profile_ledgers(
            self.portfolio, "Auren Lark", "v662-v7"
        )
        self.assertEqual(ledgers["safe-now-ledger"]["record_count"], 50)
        self.assertEqual(ledgers["candidate-ledger"]["record_count"], 30)
        self.assertEqual(ledgers["approval-gate-ledger"]["record_count"], 15)
        self.assertEqual(ledgers["skill-ledger"]["record_count"], 20)
        self.assertEqual(ledgers["runner-ledger"]["record_count"], 20)
        self.assertEqual(ledgers["clean-fix-refine-ledger"]["record_count"], 60)

    def test_profile_method_flow_retains_every_record(self) -> None:
        methods, hardening = builder.profile_method_flow(
            self.startup,
            None,
            "Auren Lark",
            "v662-v7",
            self.profile["hardening_profile"],
        )
        self.assertEqual(methods["method_count"], 22)
        self.assertEqual(methods["retained_failed_witness_count"], 22)
        self.assertEqual(hardening["rejected_fixture_count"], 14)

    def test_profile_sources_are_exact_and_https(self) -> None:
        sources = builder.profile_source_ledger(
            "Auren Lark", "v662-v7", self.profile["source_records"]
        )
        self.assertEqual(sources["record_count"], 13)
        self.assertTrue(
            all(record["url"].startswith("https://") for record in sources["records"])
        )

    def test_profile_source_http_refused(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            builder.profile_source_ledger(
                "Auren Lark",
                "v662-v7",
                [
                    {
                        "source_id": "SRC-X",
                        "title": "bad",
                        "url": "http://example.invalid",
                        "bounded_use": "none",
                    }
                ],
            )

    def test_profile_overview_uses_frozen_features(self) -> None:
        outcome = {"outcome_counts": self.profile["outcome_counts"]}
        methods, hardening = builder.profile_method_flow(
            self.startup,
            None,
            "Auren Lark",
            "v662-v7",
            self.profile["hardening_profile"],
        )
        text = builder.profile_overview_text(
            "Auren Lark",
            "v662-v7",
            outcome,
            methods,
            hardening,
            self.profile["overview_features"],
            self.profile["overview_reserved_surfaces"],
        )
        self.assertIn("declared binary byte order", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_profile_threat_model_uses_frozen_controls(self) -> None:
        text = builder.profile_threat_model_text(
            "Auren Lark", "v662-v7", self.profile["threat_controls"]
        )
        self.assertIn("Digest and DSSE checks", text)
        self.assertIn("Maori authority", text)

    def test_profile_baton_is_in_word_contract(self) -> None:
        ledgers = builder.build_profile_ledgers(
            self.portfolio, "Auren Lark", "v662-v7"
        )
        methods, _ = builder.profile_method_flow(
            self.startup,
            None,
            "Auren Lark",
            "v662-v7",
            self.profile["hardening_profile"],
        )
        text = builder.profile_baton_text(
            "Auren Lark",
            "Sable Rook",
            "v662-v7",
            "v662-v8",
            "5f89adcc5fb5fc20739f89949727245c96ca3c21",
            "9945dbb55564676e3e9a31a3cab0364cba70c365",
            self.profile,
            self.proposals["new_proposals"],
            ledgers,
            methods,
        )
        count = builder.words(text)
        self.assertGreaterEqual(count, 10000)
        self.assertLessEqual(count, 100000)
        self.assertIn("Sable Rook v662-v8 activation baton", text)
        self.assertNotIn("source_thread_id", text)

    def test_x1_profile_matches_frozen_proposal_total(self) -> None:
        self.assertEqual(self.profile["proposal_total"], 3650)
        self.assertEqual(self.proposals["new_frozen_total"], 3650)
        self.assertEqual(len(self.proposals["new_proposals"]), 20)
        self.assertEqual(self.profile["outcome_counts"], self.proposals["intended_new_outcomes"])

    def test_runner_callables_are_exact_and_unique(self) -> None:
        callables = self.profile["runner_callables"]
        self.assertEqual(len(callables), 10)
        self.assertEqual(len(callables), len(set(callables)))
        self.assertTrue(all(callable(getattr(toolkit, name)) for name in callables))


if __name__ == "__main__":
    unittest.main(verbosity=2)
