#!/usr/bin/env python3
"""Validate the Trinity extension and MCP catalogs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_EXTENSION_KINDS = {"system", "skill", "artifact"}
ALLOWED_EXTENSION_STATUS = {"active", "verified_live", "verified_live_read", "verified_live_write", "skill_only", "staged_setup_gate"}
ALLOWED_MCP_STATUS = {"verified_live", "verified_live_read", "verified_live_write", "staged_setup_gate", "skill_only", "future_candidate", "absent"}


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Trinity Extension Catalog Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- extension_count: `{payload['extension_count']}`",
        "",
        "## Failures",
    ]
    lines.extend([f"- {item}" for item in payload["failures"]] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in payload["warnings"]] or ["- none"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Trinity extension and MCP catalogs.")
    parser.add_argument("--manifest", default="docs/trinity-expansion-system-manifest-v4.json")
    parser.add_argument("--extension-catalog", default="docs/trinity-extension-catalog-v2.json")
    parser.add_argument("--mcp-catalog", default="docs/trinity-mcp-catalog-v2.json")
    parser.add_argument("--reports-dir", default="docs/trinity-extension-catalog-runs")
    parser.add_argument("--latest-json", default="docs/trinity-extension-catalog-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-extension-catalog-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    manifest = json.loads(_repo_path(args.manifest).read_text(encoding="utf-8"))
    extension_catalog = json.loads(_repo_path(args.extension_catalog).read_text(encoding="utf-8"))
    mcp_catalog = json.loads(_repo_path(args.mcp_catalog).read_text(encoding="utf-8"))

    manifest_ids = {
        str(entry.get("system_id"))
        for entry in manifest.get("systems", [])
        if isinstance(entry, dict) and entry.get("system_id")
    }
    manifest_by_pack: dict[str, int] = {}
    for entry in manifest.get("systems", []):
        if not isinstance(entry, dict):
            continue
        pack = str(entry.get("pack") or "")
        if pack and not pack.startswith("legacy_"):
            manifest_by_pack[pack] = manifest_by_pack.get(pack, 0) + 1

    extension_rows = extension_catalog.get("extensions", [])
    if not isinstance(extension_rows, list):
        failures.append("extension catalog extensions must be a list")
        extension_rows = []
    if isinstance(extension_rows, list) and len(extension_rows) != 180:
        failures.append(f"extension catalog expected 180 entries, found {len(extension_rows)}")

    extension_ids: set[str] = set()
    pack_counts: dict[str, dict[str, int]] = {}
    for index, entry in enumerate(extension_rows):
        label = f"extensions[{index}]"
        if not isinstance(entry, dict):
            failures.append(f"{label} must be an object")
            continue
        for field in ("extension_id", "extension_kind", "pack", "status", "source_of_truth"):
            if field not in entry:
                failures.append(f"{label} missing field: {field}")
        extension_id = str(entry.get("extension_id") or "").strip()
        kind = str(entry.get("extension_kind") or "").strip()
        pack = str(entry.get("pack") or "").strip()
        status = str(entry.get("status") or "").strip()
        if not extension_id:
            failures.append(f"{label} empty extension_id")
        elif extension_id in extension_ids:
            failures.append(f"duplicate extension_id: {extension_id}")
        else:
            extension_ids.add(extension_id)
        if kind not in ALLOWED_EXTENSION_KINDS:
            failures.append(f"{extension_id or label} invalid extension_kind: {kind}")
        if status not in ALLOWED_EXTENSION_STATUS:
            failures.append(f"{extension_id or label} invalid status: {status}")
        if pack:
            bucket = pack_counts.setdefault(pack, {"system": 0, "skill": 0, "artifact": 0})
            if kind in bucket:
                bucket[kind] += 1
        if kind == "system" and extension_id not in manifest_ids:
            failures.append(f"system missing from manifest: {extension_id}")

    for pack, counts in pack_counts.items():
        if pack.startswith("legacy_"):
            continue
        if counts.get("system") != 6:
            failures.append(f"{pack} expected 6 systems, found {counts.get('system')}")
        if counts.get("skill") != 2:
            failures.append(f"{pack} expected 2 skills, found {counts.get('skill')}")
        if counts.get("artifact") != 4:
            failures.append(f"{pack} expected 4 artifacts, found {counts.get('artifact')}")
        if manifest_by_pack.get(pack, 0) != 6:
            failures.append(f"{pack} expected 6 manifest systems, found {manifest_by_pack.get(pack, 0)}")

    connector_rows = mcp_catalog.get("connectors", [])
    if not isinstance(connector_rows, list):
        failures.append("mcp catalog connectors must be a list")
        connector_rows = []
    seen_connectors: set[str] = set()
    for index, entry in enumerate(connector_rows):
        label = f"connectors[{index}]"
        if not isinstance(entry, dict):
            failures.append(f"{label} must be an object")
            continue
        for field in ("mcp_id", "status", "cache_artifact", "setup_gate", "desired_state", "actual_state", "live_read_enabled", "live_write_enabled", "promotion_evidence", "blockers"):
            if field not in entry:
                failures.append(f"{label} missing field: {field}")
        connector_id = str(entry.get("mcp_id") or "").strip()
        status = str(entry.get("status") or "").strip()
        if not connector_id:
            failures.append(f"{label} empty mcp_id")
        elif connector_id in seen_connectors:
            failures.append(f"duplicate mcp_id: {connector_id}")
        else:
            seen_connectors.add(connector_id)
        if status not in ALLOWED_MCP_STATUS:
            failures.append(f"{connector_id or label} invalid mcp status: {status}")
        if not isinstance(entry.get("live_read_enabled"), bool):
            failures.append(f"{connector_id or label} live_read_enabled must be boolean")
        if not isinstance(entry.get("live_write_enabled"), bool):
            failures.append(f"{connector_id or label} live_write_enabled must be boolean")
        if not isinstance(entry.get("promotion_evidence"), list):
            failures.append(f"{connector_id or label} promotion_evidence must be a list")
        if not isinstance(entry.get("blockers"), list):
            failures.append(f"{connector_id or label} blockers must be a list")
        if bool(entry.get("live_write_enabled")) and not entry.get("promotion_evidence"):
            failures.append(f"{connector_id or label} live_write_enabled requires promotion_evidence")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "extension_count": len(extension_rows),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-trinity-extension-catalog-validation.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-extension-catalog-validation.md"
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    markdown = _markdown(payload)
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"effective_success={payload['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
