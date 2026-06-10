#!/usr/bin/env python3
"""Repair temp-only CLI bridge output surfaces for notifier compatibility."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SENSITIVE_RE = re.compile(
    "|".join(
        [
            r"BEGIN (?:RSA|OPENSSH|PRIVATE) KEY",
            r"\b(?:sk|ghp|xoxb)_[A-Za-z0-9_-]{10,}",
            r"\b[A-Z]:\\Users\\",
            r"\b[A-Z]:\\GHC-Archives\\",
            r"session(?:_|-)?jsonl",
            r"Screenshot 20\d\d",
        ]
    ),
    re.IGNORECASE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def parse_source_map(entries: list[str] | None) -> dict[str, str]:
    source_map: dict[str, str] = {}
    for entry in entries or []:
        if "=" not in entry:
            raise ValueError(f"Invalid --bridge-source entry: {entry!r}. Expected Lane=filename.")
        lane, filename = entry.split("=", 1)
        source_map[lane.strip()] = filename.strip()
    return source_map


def safe_lane_prefix(lane: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", lane)


def find_source(output_dir: Path, lane: str, source_map: dict[str, str]) -> Path | None:
    explicit = source_map.get(lane)
    if explicit:
        return output_dir / explicit
    expected = output_dir / f"{lane}-last-message.txt"
    prefix = safe_lane_prefix(lane)
    candidates = [
        path
        for path in output_dir.glob(f"{prefix}*last-message.txt")
        if path.name != expected.name and path.is_file()
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def lane_repair(output_dir: Path, lane: str, source_map: dict[str, str], allow_overwrite: bool) -> dict[str, Any]:
    expected = output_dir / f"{lane}-last-message.txt"
    source = find_source(output_dir, lane, source_map)
    if source is None or not source.exists():
        return {
            "lane": lane,
            "repair_status": "OPEN_GAP_BRIDGE_SOURCE_MISSING",
            "source_bytes": 0,
            "expected_bytes": expected.stat().st_size if expected.exists() else 0,
            "source_hash": None,
            "expected_hash": sha256_text(read_text(expected)) if expected.exists() else None,
            "strict_sensitive_or_path_marker_count": 0,
            "raw_output_boundary": "temp_only_not_published",
        }

    source_text = read_text(source)
    source_hash = sha256_text(source_text) if source_text else None
    expected_text = read_text(expected)
    expected_hash = sha256_text(expected_text) if expected_text else None
    marker_count = len(SENSITIVE_RE.findall(source_text))
    if not source_text:
        status = "OPEN_GAP_BRIDGE_SOURCE_EMPTY"
    elif marker_count:
        status = "OPEN_GAP_BRIDGE_SOURCE_MARKER_REVIEW"
    elif expected.exists() and expected_hash == source_hash:
        status = "PASS_EXPECTED_FINAL_MESSAGE_ALREADY_READY"
    elif expected.exists() and not allow_overwrite:
        status = "OPEN_GAP_EXPECTED_FINAL_MESSAGE_EXISTS_DIFFERENT_HASH"
    else:
        shutil.copyfile(source, expected)
        expected_text = read_text(expected)
        expected_hash = sha256_text(expected_text) if expected_text else None
        status = "PASS_EXPECTED_FINAL_MESSAGE_REPAIRED"

    return {
        "lane": lane,
        "repair_status": status,
        "source_bytes": source.stat().st_size,
        "expected_bytes": expected.stat().st_size if expected.exists() else 0,
        "source_hash": source_hash,
        "expected_hash": expected_hash,
        "strict_sensitive_or_path_marker_count": marker_count,
        "raw_output_boundary": "temp_only_not_published",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} CLI Bridge Surface Repair",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['overall_status']}`",
        "",
        "Lane repairs:",
    ]
    for lane in payload["lanes"]:
        lines.append(
            f"- {lane['lane']}: `{lane['repair_status']}`, source bytes `{lane['source_bytes']}`, "
            f"expected bytes `{lane['expected_bytes']}`, strict markers `{lane['strict_sensitive_or_path_marker_count']}`"
        )
    lines.extend(
        [
            "",
            "This receipt records temp-only bridge surface repair status. It does not publish raw lane text.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--lane", action="append", required=True)
    parser.add_argument("--bridge-source", action="append", help="Explicit Lane=filename source mapping.")
    parser.add_argument("--allow-overwrite", action="store_true")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    source_map = parse_source_map(args.bridge_source)
    lanes = [lane_repair(output_dir, lane, source_map, args.allow_overwrite) for lane in args.lane]
    all_pass = all(str(row["repair_status"]).startswith("PASS") for row in lanes)
    payload: dict[str, Any] = {
        "artifact_type": "cli_bridge_surface_repair",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_BRIDGE_SURFACE_REPAIR" if all_pass else "OPEN_GAP_BRIDGE_SURFACE_REPAIR",
        "lanes": lanes,
        "mutation_scope": "temp_only_expected_final_message_surface",
        "repo_mutation": False,
        "raw_output_published": False,
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
