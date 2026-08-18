#!/usr/bin/env python3
"""Exact owner-delta tests for Sable Rook v662-v8."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ghc_family_owner_delta_toolkit import (
    DeltaError,
    hardening_payload_for_profile,
    strict_json_loads,
    validate_authentication_results_shape,
    validate_dcat_distribution_descriptor,
    validate_grpc_status_trailers,
    validate_mta_sts_policy,
    validate_openpgp_one_pass_sequence,
    validate_otel_baggage_members,
    validate_problem_details_shape,
    validate_rdf_canonicalization_descriptor,
    validate_security_txt_fields,
    validate_shacl_report_shape,
    validate_sparql_result_bindings,
    validate_sse_event_block,
    validate_ttml_time_expression,
    validate_xmp_identifier_lineage,
)


DECLARED_REPOSITORY_DEPENDENCIES = [
    "scripts/ghc_family_owner_delta_phase_builder.py",
    "scripts/ghc_family_owner_delta_toolkit.py",
]

SOURCE = "23ec65060442bdaca0f03ed6f17f12da42909f5d"
X1 = "2c676073c61019ba86430adbc75cbebedec16ca1"
PHASE_ROOT = "docs/sable-rook/v662-v8"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def x1_json(name: str) -> dict:
    raw = git("show", f"{X1}:{PHASE_ROOT}/x1/{name}")
    return strict_json_loads(raw, name)


class TestImmutableX1(unittest.TestCase):
    def test_x1_is_direct_child_of_source(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1}^").strip(), SOURCE)

    def test_x1_has_eight_json_files_only(self) -> None:
        paths = git("ls-tree", "-r", "--name-only", X1, "--", f"{PHASE_ROOT}/x1").splitlines()
        self.assertEqual(len(paths), 8)
        self.assertTrue(all(path.endswith(".json") for path in paths))

    def test_x1_contains_no_x2_path(self) -> None:
        paths = git("diff", "--name-only", SOURCE, X1).splitlines()
        self.assertTrue(paths)
        self.assertTrue(all("/x1/" in f"/{path}/" for path in paths))

    def test_x1_all_strict_json(self) -> None:
        for name in (
            "builder-profile.json",
            "phase-charter.json",
            "portfolio-freeze.json",
            "proposal-freeze.json",
            "source-verification.json",
            "sparse-lane-receipt.json",
            "startup-method-flow.json",
            "workflow-plan.json",
        ):
            self.assertIsInstance(x1_json(name), dict)

    def test_proposal_counts(self) -> None:
        proposal = x1_json("proposal-freeze.json")
        self.assertEqual(proposal["inherited_frozen_baseline"], 3650)
        self.assertEqual(proposal["new_frozen_total"], 3670)
        self.assertEqual(len(proposal["selected_inherited"]), 20)
        self.assertEqual(len(proposal["new_proposals"]), 20)

    def test_outcome_counts(self) -> None:
        proposal = x1_json("proposal-freeze.json")
        counts = Counter(row["expected_disposition"] for row in proposal["new_proposals"])
        self.assertEqual(counts, Counter(completed=14, represented=4, open_gap=1, exact_gate=1))

    def test_core_proposal_fields(self) -> None:
        required = {
            "proposal_id",
            "title",
            "hypothesis",
            "null_or_failure",
            "approval_class",
            "execution_lane",
            "primary_source_needs",
            "concrete_artifacts",
            "acceptance_or_falsifier",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in x1_json("proposal-freeze.json")["new_proposals"]:
            self.assertEqual(set(row), required)
            self.assertTrue(all(row[field] for field in required))

    def test_portfolio_counts(self) -> None:
        p = x1_json("portfolio-freeze.json")
        self.assertEqual((len(p["safe_now"]["owner_execution"]), len(p["safe_now"]["successor_recommendation"])), (30, 20))
        self.assertEqual((len(p["candidate"]["owner_execution"]), len(p["candidate"]["successor_recommendation"])), (15, 15))
        self.assertEqual((len(p["approval_gates"]["exact"]), len(p["approval_gates"]["blocked"])), (10, 5))
        self.assertEqual((len(p["skills"]["owner_build"]), len(p["skills"]["successor_recommendation"])), (10, 10))
        self.assertEqual((len(p["runners"]["owner_build"]), len(p["runners"]["successor_recommendation"])), (10, 10))
        self.assertEqual((len(p["clean_fix_refine"]["owner_execution"]), len(p["clean_fix_refine"]["successor_recommendation"])), (30, 30))

    def test_profile_baseline_and_route(self) -> None:
        profile = x1_json("builder-profile.json")
        self.assertEqual(profile["activation_baseline"]["effective_negatives"], 23199)
        self.assertEqual(profile["activation_baseline"]["effective_methods"], 7793)
        self.assertEqual(profile["next_owner"], "Caelen Ash")
        self.assertEqual(profile["next_phase"], "v663-v1")
        self.assertEqual(profile["hardening_profile"], "sable-v662-v8")

    def test_sparse_contract(self) -> None:
        sparse = x1_json("sparse-lane-receipt.json")
        self.assertTrue(sparse["sparse_initialized_before_checkout"])
        self.assertEqual(sparse["initial_materialized_file_count"], 4)
        self.assertEqual(sparse["hard_rotation_threshold"], 2000)
        self.assertEqual(len(sparse["patterns"]), 6)

    def test_startup_failures_preserved(self) -> None:
        flow = x1_json("startup-method-flow.json")
        self.assertEqual(flow["retained_operational_negative_count"], 8)
        self.assertEqual(flow["passing_witness_count"], 8)
        self.assertEqual(len(flow["records"]), 8)
        self.assertEqual(len({row["method_id"] for row in flow["records"]}), 8)


class TestRdfAndResultShapes(unittest.TestCase):
    def test_rdf_descriptor_positive(self) -> None:
        result = validate_rdf_canonicalization_descriptor({"algorithm": "RDFC-1.0", "hash_algorithm": "sha384", "maximum_n_degree_calls": 4, "dataset_present": False, "canonical_output_present": False})
        self.assertFalse(result["dataset_canonicalized"])

    def test_rdf_descriptor_rejects_dataset(self) -> None:
        with self.assertRaises(DeltaError):
            validate_rdf_canonicalization_descriptor({"algorithm": "RDFC-1.0", "hash_algorithm": "sha256", "maximum_n_degree_calls": 4, "dataset_present": True, "canonical_output_present": False})

    def test_rdf_descriptor_rejects_boolean_budget(self) -> None:
        with self.assertRaises(DeltaError):
            validate_rdf_canonicalization_descriptor({"algorithm": "RDFC-1.0", "hash_algorithm": "sha256", "maximum_n_degree_calls": True, "dataset_present": False, "canonical_output_present": False})

    def test_shacl_conforming_positive(self) -> None:
        self.assertTrue(validate_shacl_report_shape({"conforms": True, "results": []})["valid"])

    def test_shacl_nonconforming_positive(self) -> None:
        report = {"conforms": False, "results": [{"severity": "sh:Violation", "focus_node": "ex:item", "source_constraint_component": "sh:ClassConstraintComponent"}]}
        self.assertEqual(validate_shacl_report_shape(report)["result_count"], 1)

    def test_shacl_rejects_missing_mandatory_field(self) -> None:
        with self.assertRaises(DeltaError):
            validate_shacl_report_shape({"conforms": False, "results": [{"severity": "sh:Violation", "focus_node": "ex:item"}]})

    def test_sparql_ask_positive(self) -> None:
        self.assertEqual(validate_sparql_result_bindings({"head": {"vars": []}, "boolean": False})["form"], "ASK")

    def test_sparql_select_positive(self) -> None:
        payload = {"head": {"vars": ["item"]}, "results": {"bindings": [{"item": {"type": "uri", "value": "https://example.invalid/item"}}]}}
        self.assertEqual(validate_sparql_result_bindings(payload)["binding_count"], 1)

    def test_sparql_rejects_mixed_forms(self) -> None:
        with self.assertRaises(DeltaError):
            validate_sparql_result_bindings({"head": {"vars": []}, "boolean": True, "results": {"bindings": []}})

    def test_dcat_positive(self) -> None:
        record = {"access_urls": ["https://example.invalid/item"], "download_urls": [], "media_type": "application/json", "checksum": {"algorithm": "sha256", "value": "00" * 32}}
        self.assertFalse(validate_dcat_distribution_descriptor(record)["url_dereferenced"])

    def test_dcat_rejects_credentials(self) -> None:
        record = {"access_urls": ["https://user@example.invalid/item"], "download_urls": [], "media_type": "application/json", "checksum": {"algorithm": "sha256", "value": "00" * 32}}
        with self.assertRaises(DeltaError):
            validate_dcat_distribution_descriptor(record)

    def test_dcat_rejects_bad_checksum(self) -> None:
        record = {"access_urls": ["https://example.invalid/item"], "download_urls": [], "media_type": "application/json", "checksum": {"algorithm": "sha256", "value": "00"}}
        with self.assertRaises(DeltaError):
            validate_dcat_distribution_descriptor(record)


class TestProtocolShapes(unittest.TestCase):
    def test_openpgp_single_positive(self) -> None:
        result = validate_openpgp_one_pass_sequence(["one_pass:alpha:last", "literal", "signature:alpha"])
        self.assertFalse(result["signature_verified"])

    def test_openpgp_nested_positive(self) -> None:
        packets = ["one_pass:alpha:more", "one_pass:beta:last", "literal", "signature:beta", "signature:alpha"]
        self.assertEqual(validate_openpgp_one_pass_sequence(packets)["one_pass_packets"], 2)

    def test_openpgp_rejects_orphan_signature(self) -> None:
        with self.assertRaises(DeltaError):
            validate_openpgp_one_pass_sequence(["literal", "signature:alpha"])

    def test_sse_positive(self) -> None:
        rows = [{"name": "data", "value": "one"}, {"name": "data", "value": "two"}, {"name": "id", "value": "evt-1"}]
        self.assertEqual(validate_sse_event_block(rows)["data_line_count"], 2)

    def test_sse_rejects_missing_data(self) -> None:
        with self.assertRaises(DeltaError):
            validate_sse_event_block([{"name": "event", "value": "update"}])

    def test_sse_rejects_excessive_retry(self) -> None:
        with self.assertRaises(DeltaError):
            validate_sse_event_block([{"name": "data", "value": "x"}, {"name": "retry", "value": "600001"}])

    def test_grpc_positive_success(self) -> None:
        self.assertEqual(validate_grpc_status_trailers({"grpc-status": "0"})["status"], 0)

    def test_grpc_positive_failure(self) -> None:
        result = validate_grpc_status_trailers({"grpc-status": "3", "grpc-message": "bad%20input", "grpc-status-details-bin": "YWJj"})
        self.assertFalse(result["details_decoded"])

    def test_grpc_rejects_success_details(self) -> None:
        with self.assertRaises(DeltaError):
            validate_grpc_status_trailers({"grpc-status": "0", "grpc-status-details-bin": "YWJj"})

    def test_problem_positive(self) -> None:
        result = validate_problem_details_shape({"type": "about:blank", "title": "Synthetic", "status": 400, "extensions": {"retryable": False}})
        self.assertFalse(result["http_served"])

    def test_problem_rejects_secret_marker(self) -> None:
        with self.assertRaises(DeltaError):
            validate_problem_details_shape({"type": "about:blank", "title": "Synthetic", "status": 500, "detail": "password=synthetic"})

    def test_problem_rejects_nested_extension(self) -> None:
        with self.assertRaises(DeltaError):
            validate_problem_details_shape({"type": "about:blank", "title": "Synthetic", "status": 400, "extensions": {"nested": {"x": 1}}})


class TestMetadataAndTime(unittest.TestCase):
    def valid_xmp(self) -> dict:
        return {"document_id": "xmp.did:document-1", "instance_id": "xmp.iid:instance-2", "original_document_id": "xmp.oid:original-1", "history": [{"event_id": "evt-create", "parent_event_id": None, "action": "created"}, {"event_id": "evt-revise", "parent_event_id": "evt-create", "action": "revised"}]}

    def test_xmp_positive(self) -> None:
        self.assertFalse(validate_xmp_identifier_lineage(self.valid_xmp())["authenticity_verified"])

    def test_xmp_rejects_forward_parent(self) -> None:
        row = self.valid_xmp()
        row["history"][0]["parent_event_id"] = "evt-future"
        with self.assertRaises(DeltaError):
            validate_xmp_identifier_lineage(row)

    def test_xmp_rejects_duplicate_event(self) -> None:
        row = self.valid_xmp()
        row["history"][1]["event_id"] = "evt-create"
        with self.assertRaises(DeltaError):
            validate_xmp_identifier_lineage(row)

    def test_ttml_offset_positive(self) -> None:
        row = {"begin": "0s", "end": "2.5s", "frame_rate": 30, "tick_rate": 1000, "region": "caption", "known_regions": ["caption"]}
        self.assertFalse(validate_ttml_time_expression(row)["media_rendered"])

    def test_ttml_clock_positive(self) -> None:
        row = {"begin": "00:00:00:00", "end": "00:00:01:15", "frame_rate": 30, "tick_rate": 1000, "region": "caption", "known_regions": ["caption"]}
        self.assertEqual(validate_ttml_time_expression(row)["end_seconds"], 1.5)

    def test_ttml_rejects_out_of_range_frame(self) -> None:
        row = {"begin": "00:00:00:00", "end": "00:00:01:30", "frame_rate": 30, "tick_rate": 1000, "region": "caption", "known_regions": ["caption"]}
        with self.assertRaises(DeltaError):
            validate_ttml_time_expression(row)

    def test_baggage_positive(self) -> None:
        result = validate_otel_baggage_members([{"key": "trace.item", "value": "bounded%20value", "properties": ["privacy=bounded"]}])
        self.assertFalse(result["telemetry_propagated"])

    def test_baggage_rejects_bad_escape(self) -> None:
        with self.assertRaises(DeltaError):
            validate_otel_baggage_members([{"key": "trace.item", "value": "bad%ZZ", "properties": []}])

    def test_baggage_rejects_control(self) -> None:
        with self.assertRaises(DeltaError):
            validate_otel_baggage_members([{"key": "trace.item", "value": "bad\nvalue", "properties": []}])


class TestMailAndDisclosureShapes(unittest.TestCase):
    def test_auth_results_positive(self) -> None:
        row = {"authserv_id": "mail.example.invalid", "results": [{"method": "spf", "result": "none", "properties": {"smtp.mailfrom": "example.invalid"}}]}
        self.assertFalse(validate_authentication_results_shape(row)["message_authenticated"])

    def test_auth_results_rejects_control(self) -> None:
        row = {"authserv_id": "mail.example.invalid", "results": [{"method": "spf", "result": "none", "properties": {"smtp.mailfrom": "bad\nvalue"}}]}
        with self.assertRaises(DeltaError):
            validate_authentication_results_shape(row)

    def test_auth_results_rejects_property_name(self) -> None:
        row = {"authserv_id": "mail.example.invalid", "results": [{"method": "spf", "result": "none", "properties": {"bad": "value"}}]}
        with self.assertRaises(DeltaError):
            validate_authentication_results_shape(row)

    def test_mta_testing_positive(self) -> None:
        policy = {"version": "STSv1", "mode": "testing", "mx": ["*.example.invalid"], "max_age": 86400, "previous_mode": "none"}
        self.assertFalse(validate_mta_sts_policy(policy)["policy_deployed"])

    def test_mta_none_positive(self) -> None:
        policy = {"version": "STSv1", "mode": "none", "mx": [], "max_age": 0, "previous_mode": "testing"}
        self.assertEqual(validate_mta_sts_policy(policy)["mode"], "none")

    def test_mta_rejects_boolean_age(self) -> None:
        policy = {"version": "STSv1", "mode": "testing", "mx": ["mx.example.invalid"], "max_age": True, "previous_mode": "none"}
        with self.assertRaises(DeltaError):
            validate_mta_sts_policy(policy)

    def valid_security_txt(self) -> dict:
        return {"contact": ["mailto:security@example.invalid"], "expires": "2030-01-01T00:00:00Z", "canonical": ["https://example.invalid/.well-known/security.txt"], "preferred_languages": ["en", "mi-NZ"]}

    def test_security_txt_positive(self) -> None:
        self.assertFalse(validate_security_txt_fields(self.valid_security_txt())["published"])

    def test_security_txt_rejects_bad_expiry(self) -> None:
        row = self.valid_security_txt()
        row["expires"] = "2030-02-30T00:00:00Z"
        with self.assertRaises(DeltaError):
            validate_security_txt_fields(row)

    def test_security_txt_rejects_fragment(self) -> None:
        row = self.valid_security_txt()
        row["canonical"] = ["https://example.invalid/.well-known/security.txt#x"]
        with self.assertRaises(DeltaError):
            validate_security_txt_fields(row)


class TestCompatibilityAndHardening(unittest.TestCase):
    def test_sable_hardening_counts(self) -> None:
        payload = hardening_payload_for_profile("sable-v662-v8")
        self.assertEqual(payload["negative_fixture_count"], 14)
        self.assertEqual(payload["rejected_fixture_count"], 14)
        self.assertEqual(payload["positive_fixture_count"], 14)
        self.assertEqual(payload["passing_fixture_count"], 14)
        self.assertTrue(payload["valid"])

    def test_sable_hardening_ids_unique(self) -> None:
        records = hardening_payload_for_profile("sable-v662-v8")["records"]
        self.assertEqual(len({row["fixture_id"] for row in records}), 14)

    def test_sable_hardening_boundaries_false(self) -> None:
        payload = hardening_payload_for_profile("sable-v662-v8")
        for field in ("rdf_dataset_canonicalized", "graph_processed", "query_executed", "url_dereferenced", "signature_verified", "network_accessed", "media_rendered", "telemetry_propagated", "mail_authenticated", "policy_deployed", "privacy_complete", "accessibility_complete", "professional_authority", "cultural_authority", "exhaustive_security"):
            self.assertIs(payload[field], False)

    def test_runner_contract_bindings_match_frozen_surfaces(self) -> None:
        expected = [
            "validate_rdf_canonicalization_descriptor",
            "validate_sparql_result_bindings",
            "validate_openpgp_one_pass_sequence",
            "validate_sse_event_block",
            "validate_grpc_status_trailers",
            "validate_xmp_identifier_lineage",
            "validate_ttml_time_expression",
            "validate_authentication_results_shape",
            "validate_security_txt_fields",
            "sable_hardening_payload",
        ]
        actual = []
        for index in range(1, 11):
            path = ROOT / PHASE_ROOT / "runners" / f"s6628-rn-{index:03d}.json"
            actual.append(strict_json_loads(path.read_bytes())["callable"])
        self.assertEqual(actual, expected)

    def test_auren_profile_compatibility(self) -> None:
        payload = hardening_payload_for_profile("auren-v662-v7")
        self.assertEqual(payload["rejected_fixture_count"], 14)
        self.assertTrue(payload["valid"])

    def test_ilyra_profile_compatibility(self) -> None:
        payload = hardening_payload_for_profile("ilyra-v662-v6")
        self.assertEqual(payload["rejected_fixture_count"], 14)
        self.assertTrue(payload["valid"])

    def test_unknown_profile_rejected(self) -> None:
        with self.assertRaises(DeltaError):
            hardening_payload_for_profile("unknown-owner")


if __name__ == "__main__":
    unittest.main(verbosity=2)
