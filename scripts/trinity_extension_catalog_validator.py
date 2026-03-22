#!/usr/bin/env python3
"""Validate the Trinity extension and MCP catalogs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_EXTENSION_COUNT = 1872
ALLOWED_EXTENSION_KINDS = {"system", "skill", "artifact"}
ALLOWED_EXTENSION_STATUS = {"active", "verified_live", "verified_live_read", "verified_live_write", "skill_only", "staged_setup_gate"}
ALLOWED_MCP_STATUS = {"verified_live", "verified_live_read", "verified_live_write", "staged_setup_gate", "skill_only", "future_candidate", "absent"}
PACK_LAYOUT_RULES = {
    "standard_pack_v17": {"system": 6, "skill": 2, "artifact": 4, "manifest_systems": 6},
    "balanced_wave_bucket_v20": {"system": 3, "skill": 0, "artifact": 12, "manifest_systems": 3},
}


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
    parser.add_argument("--manifest", default="docs/trinity-expansion-system-manifest-v17.json")
    parser.add_argument("--extension-catalog", default="docs/trinity-extension-catalog-v15.json")
    parser.add_argument("--mcp-catalog", default="docs/trinity-mcp-catalog-v11.json")
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
    if isinstance(extension_rows, list) and len(extension_rows) != EXPECTED_EXTENSION_COUNT:
        failures.append(f"extension catalog expected {EXPECTED_EXTENSION_COUNT} entries, found {len(extension_rows)}")

    extension_ids: set[str] = set()
    pack_counts: dict[str, dict[str, int]] = {}
    pack_layouts: dict[str, str] = {}
    for index, entry in enumerate(extension_rows):
        label = f"extensions[{index}]"
        if not isinstance(entry, dict):
            failures.append(f"{label} must be an object")
            continue
        for field in ("extension_id", "extension_kind", "pack", "status", "source_of_truth", "live_dependency", "history_scope", "mirror_target", "autonomy_class", "command_surface", "materialization_dependency", "authority_class", "executor_role", "authority_scope", "induction_dependency", "mirror_surface", "privacy_class", "synthetic_mesh_dependency", "authority_surface", "workbench_dependency", "induction_effect", "storage_dependency", "archive_scope", "workbench_surface", "retention_dependency", "public_source_only", "continuity_scope", "historical_reconstruction", "supplemental_only", "api_surface_binding", "agent_mesh_binding", "parallel_safety_class", "codex_scope"):
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
            layout = str(entry.get("pack_layout") or "standard_pack_v17").strip()
            if layout not in PACK_LAYOUT_RULES:
                failures.append(f"{pack} invalid pack_layout: {layout}")
            existing_layout = pack_layouts.get(pack)
            if existing_layout and existing_layout != layout:
                failures.append(f"{pack} has conflicting pack_layout values: {existing_layout} vs {layout}")
            else:
                pack_layouts[pack] = layout
            bucket = pack_counts.setdefault(pack, {"system": 0, "skill": 0, "artifact": 0})
            if kind in bucket:
                bucket[kind] += 1
        if kind == "system" and extension_id not in manifest_ids:
            failures.append(f"system missing from manifest: {extension_id}")

    for pack, counts in pack_counts.items():
        if pack.startswith("legacy_"):
            continue
        layout = pack_layouts.get(pack, "standard_pack_v17")
        expected = PACK_LAYOUT_RULES[layout]
        if counts.get("system") != expected["system"]:
            failures.append(f"{pack} expected {expected['system']} systems, found {counts.get('system')}")
        if counts.get("skill") != expected["skill"]:
            failures.append(f"{pack} expected {expected['skill']} skills, found {counts.get('skill')}")
        if counts.get("artifact") != expected["artifact"]:
            failures.append(f"{pack} expected {expected['artifact']} artifacts, found {counts.get('artifact')}")
        if manifest_by_pack.get(pack, 0) != expected["manifest_systems"]:
            failures.append(f"{pack} expected {expected['manifest_systems']} manifest systems, found {manifest_by_pack.get(pack, 0)}")

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
        for field in ("mcp_id", "status", "cache_artifact", "setup_gate", "desired_state", "actual_state", "live_read_enabled", "live_write_enabled", "promotion_evidence", "blockers", "activation_path", "workspace_target", "proof_target", "last_verified_utc", "ladder_eligibility", "persistent_scope", "prod_scope", "rollback_scope", "uat_scope", "prod_proof_state", "ha_proof_state", "cloud_staging_scope", "archive_only", "oauth_bootstrap_state", "docker_volume_state", "fallback_mode", "operator_hold", "activation_disabled_reason", "archive_policy_state"):
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
        for text_field in ("activation_path", "workspace_target", "proof_target", "last_verified_utc", "ladder_eligibility", "persistent_scope", "prod_scope", "rollback_scope", "uat_scope", "prod_proof_state", "ha_proof_state", "cloud_staging_scope", "oauth_bootstrap_state", "docker_volume_state", "fallback_mode", "activation_disabled_reason", "archive_policy_state"):
            if not isinstance(entry.get(text_field), str):
                failures.append(f"{connector_id or label} {text_field} must be a string")
        if not isinstance(entry.get("archive_only"), bool):
            failures.append(f"{connector_id or label} archive_only must be boolean")
        if not isinstance(entry.get("operator_hold"), bool):
            failures.append(f"{connector_id or label} operator_hold must be boolean")
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
