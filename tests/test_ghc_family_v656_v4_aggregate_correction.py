#!/usr/bin/env python3
"""Aggregate-launch correction tests for Caelen Morrow v656-v4."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/caelen-morrow/v656-v4"
CORRECTION1 = "14a04ce7607a839bcbff42d6daf59a1f1f24d2ed"


def git(*args: str, binary: bool = False) -> str | bytes:
    data = subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True
    ).stdout
    return data if binary else data.decode("utf-8").strip()


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class CaelenMorrowV656V4AggregateCorrectionTests(unittest.TestCase):
    def test_repository_root_is_bound_for_test_discovery(self) -> None:
        validator = (REPO / "scripts/ghc_family_v656_v4_final_validate.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("sys.path.insert(0, str(REPO))", validator)

    def test_aggregate_failure_is_retained(self) -> None:
        negatives = read_json("truth/retained-negative-register-final.json")
        ids = {
            item["negative_id"]
            for item in negatives["final_operational_negatives"]
        }
        self.assertIn("V6564-NEG-FINAL-004", ids)
        self.assertEqual(negatives["effective_count"], 14358)

    def test_aggregate_correction_manifest_exact(self) -> None:
        manifest = read_json("validation/aggregate-correction-staged-manifest.json")
        entries = {item["path"]: item for item in manifest["entries"]}
        exclusions = {item["path"] for item in manifest["declared_exclusions"]}
        actual = set(
            filter(
                None,
                str(git("diff", "--name-only", CORRECTION1, "HEAD")).splitlines(),
            )
        )
        self.assertEqual(set(entries) | exclusions, actual)
        for path, entry in entries.items():
            data = bytes(git("show", f"HEAD:{path}", binary=True))
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_route_still_has_zero_contacts(self) -> None:
        route = read_json("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["contact_count"], 0)


if __name__ == "__main__":
    unittest.main()
