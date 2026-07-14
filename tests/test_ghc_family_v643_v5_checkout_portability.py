from __future__ import annotations

import hashlib
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ghc_family_v643_v5_checkout_portability.py"
SPEC = importlib.util.spec_from_file_location("v643_v5_checkout_portability", MODULE_PATH)
PORTABILITY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(PORTABILITY)


class TestV643V5CheckoutPortability(unittest.TestCase):
    def test_lf_materialization_preserves_semantics(self):
        lf = b'{"value": 1}\n'
        crlf = lf.replace(b"\n", b"\r\n")
        expected = hashlib.sha256(lf).hexdigest()
        self.assertEqual(PORTABILITY.materialize_payload(crlf, expected, "lf"), lf)

    def test_crlf_materialization_preserves_semantics(self):
        lf = b'{"value": 1}\n'
        expected = hashlib.sha256(lf).hexdigest()
        self.assertEqual(PORTABILITY.materialize_payload(lf, expected, "crlf"), lf.replace(b"\n", b"\r\n"))

    def test_semantic_mutation_is_rejected(self):
        expected = hashlib.sha256(b'{"value": 1}\n').hexdigest()
        with self.assertRaisesRegex(ValueError, "semantic hash mismatch"):
            PORTABILITY.materialize_payload(b'{"value": 2}\n', expected, "lf")


if __name__ == "__main__":
    unittest.main()
