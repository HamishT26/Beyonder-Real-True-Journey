#!/usr/bin/env python3
"""Validate Trinity memory-bank registry and latest sync report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "docs" / "trinity-memory-bank-registry-v3.json"
REPORT_PATH = ROOT / "docs" / "trinity-memory-bank-sync-latest.json"
OUTPUT_JSON = ROOT / "docs" / "trinity-memory-bank-validation-latest.json"
OUTPUT_MD = ROOT / "docs" / "trinity-memory-bank-validation-latest.md"

REQUIRED_SURFACES = {
    "repo",
    "github",
    "postgres",
    "docker",
    "notion",
    "linear",
    "new_project_workbench",
    "google_drive",
}

STORAGE_PRESSURE_CRITICAL_FREE_GIB = 2.0
STORAGE_PRESSURE_WATCH_FREE_GIB = 4.0


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Trinity memory-bank registry and report.")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not REGISTRY_PATH.exists():
        errors.append("registry missing")
        registry = {}
    else:
        registry = load_json(REGISTRY_PATH)

    if not REPORT_PATH.exists():
        errors.append("sync report missing")
        report = {}
    else:
        report = load_json(REPORT_PATH)

    banks = registry.get("memory_banks", []) if isinstance(registry, dict) else []
    if not isinstance(banks, list):
        errors.append("memory_banks must be a list")
        banks = []

    surface_names = {row.get("surface", "") for row in banks if isinstance(row, dict)}
    missing = sorted(REQUIRED_SURFACES - surface_names)
    if missing:
        errors.append(f"missing required surfaces: {', '.join(missing)}")

    latest_snapshot = registry.get("latest_snapshot", {}) if isinstance(registry, dict) else {}
    archive_rel = latest_snapshot.get("archive", "")
    if not archive_rel:
        errors.append("latest_snapshot.archive missing")
    else:
        archive_path = ROOT / archive_rel
        if not archive_path.exists():
            errors.append(f"latest snapshot archive not found: {archive_rel}")

    repo_row = next((row for row in banks if isinstance(row, dict) and row.get("surface") == "repo"), None)
    if repo_row and repo_row.get("status") != "authoritative":
        errors.append("repo surface must remain authoritative")

    github_row = next((row for row in banks if isinstance(row, dict) and row.get("surface") == "github"), None)
    if github_row and not github_row.get("reachable", False):
        warnings.append("github mirror is currently unreachable")

    drive_row = next((row for row in banks if isinstance(row, dict) and row.get("surface") == "google_drive"), None)
    if drive_row and drive_row.get("status") not in {"staged_with_blockers", "auth_blocked", "live_archive_mirror", "bounded_archive_mirror", "bounded_working_mirror"}:
        errors.append("google_drive status is invalid for bounded memory-bank flow")
    for row in banks:
        if not isinstance(row, dict):
            continue
        for field in ("retention_class", "archive_upload_state", "cloud_capacity_class", "last_archive_verified_utc"):
            if field not in row:
                errors.append(f"{row.get('surface', 'unknown')} missing {field}")
    for field in ("retained_snapshot_count", "prune_policy_applied_at", "storage_pressure_class"):
        if field not in registry:
            errors.append(f"registry missing {field}")
    storage_pressure = registry.get("storage_pressure", {}) if isinstance(registry, dict) else {}
    if isinstance(storage_pressure, dict):
        free_gib = float(storage_pressure.get("free_gib", 0.0) or 0.0)
        if free_gib < STORAGE_PRESSURE_CRITICAL_FREE_GIB:
            warnings.append(f"local free space critically low: {free_gib} GiB")
        elif free_gib < STORAGE_PRESSURE_WATCH_FREE_GIB:
            warnings.append(f"local free space in watch band: {free_gib} GiB")
    if int(registry.get("retained_snapshot_count", 0) or 0) < 1:
        errors.append("at least one retained memory-bank snapshot is required")
    if not str(registry.get("prune_policy_applied_at") or "").strip():
        warnings.append("prune_policy_applied_at is empty; latest prune may not have been rerun yet")

    status = "PASS"
    if errors:
        status = "FAIL"
    elif warnings:
        status = "WARN"

    payload = {
        "generated_utc": now_iso(),
        "overall_status": status,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "registry": REGISTRY_PATH.relative_to(ROOT).as_posix(),
        "report": REPORT_PATH.relative_to(ROOT).as_posix(),
    }
    write_json(OUTPUT_JSON, payload)
    write_text(
        OUTPUT_MD,
        "# Trinity Memory Bank Validation\n\n"
        f"- overall_status: `{status}`\n"
        f"- errors: `{len(errors)}`\n"
        f"- warnings: `{len(warnings)}`\n"
        + ("\n".join(f"- error: `{item}`" for item in errors) + "\n" if errors else "")
        + ("\n".join(f"- warning: `{item}`" for item in warnings) + "\n" if warnings else ""),
    )
    if status == "FAIL":
        return 1
    if status == "WARN" and args.fail_on_warn:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
