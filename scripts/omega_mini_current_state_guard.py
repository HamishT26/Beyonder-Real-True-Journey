#!/usr/bin/env python3
"""Validate the lightweight omega-mini current-state and beacon files.

The guard is intentionally narrow: it checks JSON shape, relative lookup
targets, phase pointers, and publication-boundary booleans without reading or
publishing raw lane text.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise TypeError(f"{path} did not contain a JSON object")
    return data


def require_false_map(name: str, value: Any, issues: list[str]) -> None:
    if not isinstance(value, dict):
        issues.append(f"{name} is not an object")
        return
    for key, item in value.items():
        if item is not False and item != "not_claimed":
            issues.append(f"{name}.{key} is not explicitly false/not_claimed: {item!r}")


def validate_lookup_files(root: Path, label: str, files: Any, issues: list[str]) -> None:
    if not isinstance(files, list):
        issues.append(f"{label} is not a list")
        return
    seen: set[str] = set()
    for item in files:
        if not isinstance(item, str):
            issues.append(f"{label} contains non-string entry: {item!r}")
            continue
        if item in seen:
            issues.append(f"{label} duplicates {item}")
        seen.add(item)
        if Path(item).is_absolute() or ":" in item:
            issues.append(f"{label} contains absolute or drive-qualified path: {item}")
            continue
        if not (root / item).exists():
            issues.append(f"{label} missing relative target: {item}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Omega-mini worktree root")
    parser.add_argument("--expected-phase", required=True)
    parser.add_argument("--expected-completed-x1", required=True)
    parser.add_argument("--expected-next-x1-lane", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    current_path = root / "docs" / "omega-mini-index" / "omega-mini-current-state-v1.json"
    beacon_path = root / "docs" / "omega-mini-index" / "omega-mini-latest-updates-beacon-v1.json"

    issues: list[str] = []
    current = load_json(current_path)
    beacon = load_json(beacon_path)

    if current.get("current_active_phase") != args.expected_phase:
        issues.append(
            "current_active_phase mismatch: "
            f"{current.get('current_active_phase')!r} != {args.expected_phase!r}"
        )
    if beacon.get("current_active_phase") != args.expected_phase:
        issues.append(
            "beacon current_active_phase mismatch: "
            f"{beacon.get('current_active_phase')!r} != {args.expected_phase!r}"
        )
    if current.get("latest_completed_x1_phase") != args.expected_completed_x1:
        issues.append("current latest_completed_x1_phase mismatch")
    if beacon.get("latest_completed_x1_phase") != args.expected_completed_x1:
        issues.append("beacon latest_completed_x1_phase mismatch")
    if current.get("next_x1_lane_after_x2") != args.expected_next_x1_lane:
        issues.append("current next_x1_lane_after_x2 mismatch")
    if beacon.get("next_x1_lane_after_x2") != args.expected_next_x1_lane:
        issues.append("beacon next_x1_lane_after_x2 mismatch")

    for source, label in [(current, "current"), (beacon, "beacon")]:
        heads = source.get("remote_verified_heads", {})
        if heads:
            if not isinstance(heads, dict):
                issues.append(f"{label}.remote_verified_heads is not an object")
            else:
                for key, value in heads.items():
                    if not isinstance(value, str) or not HEX40_RE.fullmatch(value):
                        issues.append(f"{label}.remote_verified_heads.{key} is not a 40-char hex sha")

    validate_lookup_files(root, "current.current_lookup_files", current.get("current_lookup_files"), issues)
    validate_lookup_files(root, "beacon.latest_lookup_files", beacon.get("latest_lookup_files"), issues)

    stale_text = json.dumps({"current": current, "beacon": beacon}, sort_keys=True)
    if "v530" in str(current.get("current_active_phase", "")):
        issues.append("current active phase still points at v530")
    if "v540-gmut-thos-v76-v5-x1, not v530" in stale_text:
        issues.append("historical row still names v5 x1 as active")

    require_false_map("current.publication_boundary", current.get("publication_boundary"), issues)
    require_false_map("current.claim_boundary", current.get("claim_boundary"), issues)
    require_false_map("beacon.publication_boundary", beacon.get("publication_boundary"), issues)
    require_false_map("beacon.claim_boundary", beacon.get("claim_boundary"), issues)

    result = {
        "schema": "ghc.omega_mini_current_state_guard.result.v1",
        "status": "PASS" if not issues else "FAIL",
        "root_name": root.name,
        "expected_phase": args.expected_phase,
        "expected_completed_x1": args.expected_completed_x1,
        "expected_next_x1_lane": args.expected_next_x1_lane,
        "current_active_phase": current.get("current_active_phase"),
        "beacon_active_phase": beacon.get("current_active_phase"),
        "lookup_file_count": {
            "current": len(current.get("current_lookup_files", []))
            if isinstance(current.get("current_lookup_files"), list)
            else None,
            "beacon": len(beacon.get("latest_lookup_files", []))
            if isinstance(beacon.get("latest_lookup_files"), list)
            else None,
        },
        "issues": issues,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
