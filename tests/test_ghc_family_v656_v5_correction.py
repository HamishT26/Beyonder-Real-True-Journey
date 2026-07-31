#!/usr/bin/env python3
"""Correction and cap tests for Eiren Kestrel v656-v5."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v656-v5"
SOURCE = "c1518e6873068f6cc20ff69a30437d69404ef057"
X1 = "e313d47c1bc6386d3dbdf1773d1d7cb4026bc7f9"
CLOSEOUT = "3181608db19f39bb7b91be01fc62e64840a86c5e"


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True
    ).stdout
    return result if binary else result.decode("utf-8").strip()


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class EirenKestrelV656V5CorrectionTests(unittest.TestCase):
    def test_immutable_x1_tree_has_no_x2_content(self) -> None:
        paths = str(git("ls-tree", "-r", "--name-only", X1)).splitlines()
        owner = [p for p in paths if p.startswith("docs/eiren-kestrel/v656-v5/")]
        self.assertFalse(any("/surfaces/" in p for p in owner))
        self.assertFalse(any("/runners/" in p for p in owner))
        proposals = json.loads(
            bytes(
                git(
                    "show",
                    f"{X1}:docs/eiren-kestrel/v656-v5/preregistration/proposals.json",
                    binary=True,
                )
            ).decode("utf-8")
        )
        self.assertFalse(
            any("observed_outcome" in item for item in proposals["proposals"])
        )

    def test_lossless_text_reference_ledgers_are_under_cap(self) -> None:
        for name in (
            "method-flow-ledger.json",
            "method-flow-ledger-x2.json",
            "method-flow-ledger-final.json",
        ):
            path = ROOT / "method-flow" / name
            ledger = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(ledger["text_reference_encoding"]["lossless"], True)
            self.assertTrue(ledger["text_dictionary"])
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_final_method_flow_and_negative_are_retained(self) -> None:
        flow = read_json("method-flow/method-flow-ledger-final.json")
        negatives = read_json("truth/retained-negative-register-final.json")
        self.assertEqual(flow["counts"]["methods"], 835)
        self.assertEqual(flow["counts"]["witness_results"]["fail"], 835)
        self.assertEqual(flow["counts"]["witness_results"]["pass"], 835)
        self.assertEqual(negatives["final_operational_count"], 9)
        self.assertEqual(negatives["effective_count"], 14549)

    def test_correction_manifest_exact(self) -> None:
        manifest = read_json("validation/correction-staged-manifest.json")
        entries = {item["path"]: item for item in manifest["entries"]}
        exclusions = {item["path"] for item in manifest["declared_exclusions"]}
        actual = set(
            filter(
                None,
                str(git("diff", "--name-only", CLOSEOUT, "HEAD")).splitlines(),
            )
        )
        self.assertEqual(set(entries) | exclusions, actual)
        for path, entry in entries.items():
            data = bytes(git("show", f"HEAD:{path}", binary=True))
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_all_owner_documents_are_under_cap(self) -> None:
        paths = str(git("diff", "--name-only", SOURCE, "HEAD")).splitlines()
        for relative in paths:
            data = bytes(git("show", f"HEAD:{relative}", binary=True))
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            self.assertLessEqual(len(text.split()), 100000, relative)

    def test_terminal_route_remains_prepared(self) -> None:
        route = read_json("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["contact_count"], 0)
        self.assertEqual(route["successor_exact_title"], "Elaren Kestrel")


if __name__ == "__main__":
    unittest.main()
