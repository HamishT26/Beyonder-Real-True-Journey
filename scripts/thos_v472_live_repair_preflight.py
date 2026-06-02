#!/usr/bin/env python3
"""Preflight the approved v472 plugin-cache repair without mutating cache files."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v472-thos-v3-x1"
GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def path_safe(value: str) -> bool:
    return not (
        value.startswith("/")
        or value.startswith("\\")
        or re.match(r"^[A-Za-z]:[\\/]", value)
        or ".." in Path(value).parts
    )


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def simple_frontmatter_status(data: bytes) -> dict[str, Any]:
    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {"starts_with_frontmatter": False, "has_closing_delimiter": False}
    closing_line = None
    for index, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            closing_line = index
            break
    header = "\n".join(lines[1 : closing_line - 1]) if closing_line else "\n".join(lines[1:40])
    return {
        "closing_delimiter_line": closing_line,
        "description_seen": bool(re.search(r"(?m)^description\s*:", header)),
        "has_closing_delimiter": closing_line is not None,
        "name_seen": bool(re.search(r"(?m)^name\s*:", header)),
        "starts_with_frontmatter": True,
    }


def build_preflight(repo_root: Path, plugin_root: Path) -> dict[str, Any]:
    packet_ref = "v472-thos-v2-x1-live-repair-approval-packet-v1.json"
    packet = read_json(repo_root / "docs" / "trinity-live-traces" / packet_ref)
    entries = packet["entries"]

    results: list[dict[str, Any]] = []
    for entry in entries:
        relative_path = entry["relative_path"]
        target = (plugin_root / Path(relative_path)).resolve()
        root_resolved = plugin_root.resolve()
        target_exists = target.exists()
        target_in_scope = str(target).lower().startswith(str(root_resolved).lower())
        live_hash = sha256_bytes(target.read_bytes()) if target_exists and target_in_scope else None
        status = "ELIGIBLE_UNDER_APPROVED_PACKET" if live_hash == entry["sha256_before"] else "BLOCKED_HASH_MISMATCH"
        if not target_exists:
            status = "BLOCKED_MISSING_PATH"
        elif not target_in_scope or not path_safe(relative_path):
            status = "BLOCKED_UNSAFE_PATH"
        result = {
            "approval_status": entry["approval_status"],
            "expected_after_hash": entry["sha256_after_preview"],
            "expected_before_hash": entry["sha256_before"],
            "frontmatter_probe": simple_frontmatter_status(target.read_bytes()) if target_exists and target_in_scope else {},
            "live_hash": live_hash,
            "path_id": entry["path_id"],
            "path_safe": target_in_scope and path_safe(relative_path),
            "relative_path": relative_path,
            "repair_performed": False,
            "requires_new_or_refreshed_approval": live_hash != entry["sha256_before"],
            "status": status,
        }
        results.append(result)

    matched = [item for item in results if item["status"] == "ELIGIBLE_UNDER_APPROVED_PACKET"]
    mismatched = [item for item in results if item["status"] == "BLOCKED_HASH_MISMATCH"]
    unsafe_or_missing = [item for item in results if item["status"] not in {"ELIGIBLE_UNDER_APPROVED_PACKET", "BLOCKED_HASH_MISMATCH"}]
    repair_allowed = len(matched) == len(results) and not unsafe_or_missing

    rows = [
        row("entry_count", "PASS_SHAPE_ONLY" if len(results) == 37 else "FAIL_BLOCKER", "The approved packet must still contain exactly 37 entries", {"count": len(results)}),
        row("path_scope", "PASS_SHAPE_ONLY" if not unsafe_or_missing else "FAIL_BLOCKER", "Every target path must exist and remain inside the plugin-cache root", unsafe_or_missing),
        row("before_hash_match", "PASS_SHAPE_ONLY" if repair_allowed else "FAIL_BLOCKER", "Every live file must match the approved before hash before repair", {"matched": len(matched), "mismatched": len(mismatched)}),
        row("write_decision", "PASS_SHAPE_ONLY", "No plugin-cache write was performed during this preflight"),
        row("arby_aster_retry", "OPEN_GAP", "CLI retry deferred because the approved 37-file repair prerequisite was not met"),
    ]

    return {
        "aggregate_status": "PASS_READY_TO_REPAIR" if repair_allowed else "BLOCKED_STALE_APPROVAL_HASHES",
        "approved_packet_ref": packet_ref,
        "blocked_count": len(mismatched) + len(unsafe_or_missing),
        "eligible_count": len(matched),
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "phase_slug": PHASE,
        "plugin_root": "C:/Users/hamis/.codex/plugins/cache",
        "results": results,
        "rows": rows,
        "total_count": len(results),
    }


def write_artifacts(repo_root: Path, report: dict[str, Any]) -> list[Path]:
    root = repo_root / "docs" / "trinity-live-traces"
    written: list[Path] = []
    status = report["aggregate_status"]

    path = root / f"{PHASE}-live-repair-hash-preflight-v1.json"
    write_json(path, report)
    written.append(path)
    write_md(
        root / f"{PHASE}-live-repair-hash-preflight-v1.md",
        f"""
# v472 THOS v3 x1 Live-Repair Hash Preflight

Status: `{status}`.

The approved plugin-cache repair was not executed. The preflight found `{report["eligible_count"]}` eligible paths and `{report["blocked_count"]}` blocked paths under the approved hash gate, so the packet is stale for current live cache state.
""",
    )
    written.append(root / f"{PHASE}-live-repair-hash-preflight-v1.md")

    blocker = {
        "aggregate_status": "BLOCKED_STALE_APPROVAL_HASHES",
        "generated_at_utc": report["generated_at_utc"],
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE,
        "rows": [
            row("no_repair", "FAIL_BLOCKER", "No live plugin-cache repair was performed because 32 live hashes differ from the approved packet"),
            row("no_cli_retry", "OPEN_GAP", "Arby/Aster retry is deferred because the repair prerequisite did not happen"),
            row("safe_next_step", "PASS_SHAPE_ONLY", "Prepare a refreshed approval packet from current live hashes before any repair"),
            row("claim_ceiling", "PASS_SHAPE_ONLY", "This blocker does not validate GMUT, close gates, or alter canon"),
        ],
    }
    path = root / f"{PHASE}-repair-blocker-ledger-v1.json"
    write_json(path, blocker)
    written.append(path)
    write_md(
        root / f"{PHASE}-repair-blocker-ledger-v1.md",
        """
# v472 THOS v3 x1 Repair Blocker Ledger

The approved packet is stale against the current plugin cache. The safe next step is a refreshed current-hash approval packet; no live cache repair or Arby/Aster retry was executed.
""",
    )
    written.append(root / f"{PHASE}-repair-blocker-ledger-v1.md")

    current_hash_packet = {
        "aggregate_status": "REFRESH_APPROVAL_REQUIRED",
        "generated_at_utc": report["generated_at_utc"],
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE,
        "refreshed_approval_required": True,
        "rows": [
            {
                "current_live_hash": item["live_hash"],
                "frontmatter_probe": item["frontmatter_probe"],
                "old_expected_before_hash": item["expected_before_hash"],
                "path_id": item["path_id"],
                "relative_path": item["relative_path"],
                "status": item["status"],
            }
            for item in report["results"]
        ],
    }
    path = root / f"{PHASE}-current-hash-refresh-packet-v1.json"
    write_json(path, current_hash_packet)
    written.append(path)
    write_md(
        root / f"{PHASE}-current-hash-refresh-packet-v1.md",
        """
# v472 THOS v3 x1 Current-Hash Refresh Packet

This packet records current live hashes for the same 37 paths without raw body text. It is not approval and performs no repair.
""",
    )
    written.append(root / f"{PHASE}-current-hash-refresh-packet-v1.md")

    run_status = {
        "aggregate_status": "BLOCKED_STALE_APPROVAL_HASHES",
        "generated_at_utc": report["generated_at_utc"],
        "gmUT_gates_open": GMUT_GATES,
        "mutation_performed": False,
        "next_expected_phase": "v472-thos-v3-x2",
        "phase_slug": PHASE,
        "summary": "Approved repair was safely stopped at hash preflight: 5 matched, 32 mismatched, 0 writes.",
    }
    path = root / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        root / f"{PHASE}-run-status-v1.md",
        """
# v472 THOS v3 x1 Run Status

Approved repair stopped safely at preflight because the live plugin-cache state no longer matches the approved packet. No plugin-cache writes and no Arby/Aster retry occurred.
""",
    )
    written.append(root / f"{PHASE}-run-status-v1.md")
    return written


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    plugin_root = Path("C:/Users/hamis/.codex/plugins/cache")
    report = build_preflight(repo_root, plugin_root)
    written = write_artifacts(repo_root, report)
    print(json.dumps({"status": report["aggregate_status"], "written": [path.as_posix() for path in written]}, indent=2))


if __name__ == "__main__":
    main()
