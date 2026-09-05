"""Selected Vesper v686-v3 owner tests for frozen configuration contracts."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ghc_family_config_assurance as assurance
import ghc_family_config_layers as layers
import ghc_family_config_obligations as obligations
import ghc_family_config_toml as toml
import ghc_family_config_transaction as transaction


ROWS = json.loads(
    (ROOT / "docs/vesper-arlen/v686-v3/x1/new-proposals.json").read_text(
        encoding="utf-8"
    )
)["proposals"]
COMPUTE = {
    "toml": toml.evaluate,
    "layers": layers.evaluate,
    "transaction": transaction.evaluate,
    "assurance": assurance.evaluate,
    "obligations": obligations.evaluate,
}


class FrozenFamilies(unittest.TestCase):
    """One test per frozen family; each test checks its ten cases."""


def family_test(family: str):
    def test(self):
        selected = [row for row in ROWS if row["family"] == family]
        self.assertEqual(len(selected), 10)
        for row in selected:
            with self.subTest(proposal=row["proposal_id"]):
                before = toml.canonical(row["input"])
                result = COMPUTE[row["runner"]](
                    row["operation"], copy.deepcopy(row["input"])
                )
                self.assertEqual(
                    toml.canonical(result), toml.canonical(row["expected_result"])
                )
                self.assertEqual(before, toml.canonical(row["input"]))

    return test


for _family in sorted({row["family"] for row in ROWS}):
    setattr(FrozenFamilies, "test_" + _family, family_test(_family))


class IndependentInvariants(unittest.TestCase):
    def test_duplicate_json_member_rejected(self):
        with self.assertRaises(toml.Refusal):
            toml.strict_load('{"a":1,"a":2}')

    def test_nonfinite_json_rejected(self):
        for word in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(word=word), self.assertRaises(toml.Refusal):
                toml.strict_load(word)

    def test_lone_surrogate_rejected(self):
        with self.assertRaises(toml.Refusal):
            toml.check_json(chr(0xD800))

    def test_nonstring_mapping_key_rejected(self):
        with self.assertRaises(toml.Refusal):
            toml.check_json({1: "x"})

    def test_deep_json_tree_rejected(self):
        value = 0
        for _ in range(66):
            value = [value]
        with self.assertRaises(toml.Refusal):
            toml.check_json(value)

    def test_large_json_node_budget_rejected(self):
        with self.assertRaises(toml.Refusal):
            toml.check_json([0] * 10_001)

    def test_toml_duplicate_key_refused(self):
        self.assertEqual(
            toml.evaluate(
                "parse", {"text": "a = 1\na = 2\n", "byte_budget": 4096}
            ),
            {"error": "invalid_toml"},
        )

    def test_toml_nonfinite_refused_by_local_json_profile(self):
        self.assertEqual(
            toml.evaluate("parse", {"text": "a = nan\n", "byte_budget": 4096}),
            {"error": "invalid_toml"},
        )

    def test_toml_byte_budget_precedes_parse(self):
        self.assertEqual(
            toml.evaluate("parse", {"text": "a = 1\n", "byte_budget": 1}),
            {"error": "text_budget"},
        )

    def test_roundtrip_requires_existing_nested_parent(self):
        self.assertEqual(
            toml.evaluate(
                "roundtrip",
                {"text": "a = 1\n", "path": "b.c", "value": 2, "marker": "a"},
            ),
            {"error": "invalid_roundtrip"},
        )

    def test_layer_merge_does_not_alias_input(self):
        data = {"layers": [{"a": {"x": 1}}, {"a": {"y": 2}}], "precedence": ["a", "b"]}
        before = copy.deepcopy(data)
        result = layers.evaluate("merge", data)
        result["a"]["x"] = 9
        self.assertEqual(data, before)

    def test_origin_trace_retains_false_and_zero(self):
        result = layers.evaluate(
            "origins",
            {"layers": [{"name": "base", "values": {"zero": 0, "flag": False}}]},
        )
        self.assertEqual(result["zero"]["value"], 0)
        self.assertIs(result["flag"]["value"], False)

    def test_snapshot_base_remains_unchanged(self):
        base = {"a": 1}
        result = layers.evaluate("snapshot", {"base": base, "set": {"a": 2}})
        self.assertEqual(base, {"a": 1})
        self.assertEqual(result["derived"], {"a": 2})

    def test_atomic_change_failure_returns_no_partial_document(self):
        data = {
            "document": {"a": {}},
            "changes": [
                {"op": "set", "path": "a.x", "value": 1},
                {"op": "set", "path": "missing.x", "value": 2},
            ],
        }
        before = copy.deepcopy(data)
        self.assertEqual(transaction.evaluate("apply", data), {"error": "transaction_refused"})
        self.assertEqual(data, before)

    def test_allowlist_uses_token_ancestry(self):
        self.assertEqual(
            transaction.evaluate(
                "authorize",
                {"allowed": ["service"], "paths": ["service2.option"], "requested_by": "fixture"},
            ),
            {"error": "path_not_allowed"},
        )

    def test_rollback_chain_rejects_wrong_parent(self):
        self.assertEqual(
            transaction.evaluate(
                "chain",
                {
                    "snapshots": [{"v": 1}, {"v": 2}],
                    "links": [
                        {
                            "ordinal": 1,
                            "parent_sha256": "0" * 64,
                            "child_sha256": toml.sha({"v": 2}),
                            "reason": "fixture",
                        }
                    ],
                },
            ),
            {"error": "lineage_mismatch"},
        )

    def test_diff_distinguishes_boolean_and_integer(self):
        self.assertEqual(
            transaction.evaluate(
                "diff",
                {"before": {"a": False}, "after": {"a": 0}, "breaking_prefixes": []},
            )["paths"],
            ["a"],
        )

    def test_secret_guard_never_claims_real_secret(self):
        result = assurance.evaluate("secret_guard", {"marker": "ROTATION_REQUIRED"})
        self.assertEqual(result, {"accepted_placeholder": False, "real_secret_used": False})

    def test_environment_unknown_field_refused(self):
        self.assertEqual(
            assurance.evaluate(
                "env_overlay",
                {"values": {"OTHER": "1"}, "schema": {"PORT": "integer"}, "allowed": ["PORT"]},
            ),
            {"error": "environment_not_allowed"},
        )

    def test_schema_boolean_is_not_integer(self):
        self.assertEqual(
            assurance.evaluate(
                "schema",
                {"config": {"n": True}, "schema": {"required": ["n"], "types": {"n": "integer"}, "additional": False}},
            ),
            {"error": "type_mismatch"},
        )

    def test_receipt_extra_field_refused(self):
        expected = {"owner": "o", "phase": "p", "source": "s", "candidate": "c", "same_owner_only": True, "authority": False}
        receipt = dict(expected, extra=True)
        self.assertEqual(assurance.evaluate("receipt", {"expected": expected, "receipt": receipt}), {"error": "scope_mismatch"})

    def test_accessible_summary_reserves_manual_review(self):
        result = assurance.evaluate(
            "summary",
            {"changes": [{"path": "a", "before": False, "after": True}], "language": "en-NZ"},
        )
        self.assertTrue(result["manual_review_reserved"])
        self.assertEqual(result["rows"], ["a: false → true"])

    def test_obligation_external_action_refused(self):
        self.assertEqual(
            obligations.evaluate(
                "obligation",
                {"obligation": "fixture", "evidence": None, "authority": None, "external_action": True, "expected_disposition": "represented"},
            ),
            {"error": "unsupported_promotion"},
        )

    def test_envelope_forged_report_rejected(self):
        row = ROWS[0]
        record = toml.envelope(row, {"fiction": True})
        self.assertFalse(toml.verify_envelope(row, record, toml.evaluate)["accepted"])

    def test_envelope_numeric_authority_is_rejected(self):
        row = ROWS[0]
        record = toml.envelope(row, row["expected_result"])
        record["authority"] = 0
        self.assertFalse(toml.verify_envelope(row, record, toml.evaluate)["accepted"])


if __name__ == "__main__":
    unittest.main()
