from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ghc_family_constraint_evidence_validator.py"
SPEC = importlib.util.spec_from_file_location("constraint_validator_hash_alias", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


class TestConstraintHashAlias(unittest.TestCase):
    def test_exact_legacy_alias_is_bounded_and_warns(self):
        path = ROOT / "docs/orin-thale/v642-v6/provenance/frozen-chain-proposal-index.json"
        warnings: list[str] = []
        self.assertTrue(
            VALIDATOR.frozen_inherited_hash_matches(
                path,
                "d4b6882b5a670b2ccbe3fc2517ffd55d60e82e8b338815107c2d1d10e7b78a3b",
                warnings,
            )
        )
        self.assertEqual(len(warnings), 1)
        self.assertIn("retained historical negative", warnings[0])

    def test_alias_does_not_accept_arbitrary_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "frozen-chain-proposal-index.json"
            path.write_text("{}\n", encoding="utf-8", newline="\n")
            self.assertFalse(
                VALIDATOR.frozen_inherited_hash_matches(
                    path,
                    "d4b6882b5a670b2ccbe3fc2517ffd55d60e82e8b338815107c2d1d10e7b78a3b",
                [],
                )
            )


if __name__ == "__main__":
    unittest.main()
