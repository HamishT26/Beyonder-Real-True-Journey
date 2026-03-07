#!/usr/bin/env python3
"""Validate the Trinity expansion manifest."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_PILLARS = {"mind", "body", "heart", "trinity"}
ALLOWED_MODES = {"live", "offline"}
ALLOWED_PROFILES = {"standard", "deep", "collab", "materialize"}
ALLOWED_WAVES = {"legacy", "wave1", "wave2", "wave3", "wave4", "wave5", "wave6", "wave7", "wave8", "wave9", "wave10", "wave11", "wave12", "wave13", "wave14", "wave15", "wave16", "wave17", "wave18", "wave19", "wave20"}
ALLOWED_TRACKS = {
    "mind_theory",
    "body_compute",
    "heart_governance",
    "trinity_hardening",
    "trinity_memory_orchestration",
    "mcp_collaboration",
    "connector_ops",
    "continuity_ops",
    "release_ops",
    "compute_ecosystem",
    "identity_governance",
    "public_intelligence",
    "active_materialization",
    "os_runtime",
    "wetware_readiness",
}
ALLOWED_GATE_LEVELS = {"support", "pillar_constellation", "hardening_gate", "readiness_gate", "supercycle_gate", "pack_gate"}


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
        "# Trinity Expansion Manifest Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- systems: `{payload['system_count']}`",
        "",
        "## Failures",
    ]
    if payload["failures"]:
        lines.extend([f"- {item}" for item in payload["failures"]])
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings"])
    if payload["warnings"]:
        lines.extend([f"- {item}" for item in payload["warnings"]])
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate docs/trinity-expansion-system-manifest-v4.json")
    parser.add_argument("--manifest", default="docs/trinity-expansion-system-manifest-v4.json")
    parser.add_argument("--reports-dir", default="docs/trinity-expansion-manifest-runs")
    parser.add_argument("--latest-json", default="docs/trinity-expansion-manifest-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-expansion-manifest-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    manifest_path = _repo_path(args.manifest)
    if not manifest_path.exists():
        failures.append(f"missing manifest: {args.manifest}")
        manifest: dict[str, Any] = {}
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid json: {exc}")
            manifest = {}

    systems = manifest.get("systems", []) if isinstance(manifest, dict) else []
    if not isinstance(systems, list):
        failures.append("manifest.systems must be a list")
        systems = []
    if isinstance(systems, list) and len(systems) != 170:
        failures.append(f"manifest expected 170 systems, found {len(systems)}")

    seen_ids: set[str] = set()
    for index, entry in enumerate(systems):
        row_label = f"systems[{index}]"
        if not isinstance(entry, dict):
            failures.append(f"{row_label} must be an object")
            continue
        for field in ("system_id", "pillar", "script", "mode", "profiles", "outputs", "depends_on", "timeout_sec", "wave", "track", "gate_level", "cache_artifacts", "pack"):
            if field not in entry:
                failures.append(f"{row_label} missing field: {field}")
        system_id = str(entry.get("system_id") or "").strip()
        if not system_id:
            failures.append(f"{row_label} has empty system_id")
        elif system_id in seen_ids:
            failures.append(f"duplicate system_id: {system_id}")
        else:
            seen_ids.add(system_id)

        pillar = str(entry.get("pillar") or "").strip()
        if pillar not in ALLOWED_PILLARS:
            failures.append(f"{system_id or row_label} invalid pillar: {pillar}")

        mode = str(entry.get("mode") or "").strip()
        if mode not in ALLOWED_MODES:
            failures.append(f"{system_id or row_label} invalid mode: {mode}")

        wave = str(entry.get("wave") or "").strip()
        if wave not in ALLOWED_WAVES:
            failures.append(f"{system_id or row_label} invalid wave: {wave}")

        track = str(entry.get("track") or "").strip()
        if track not in ALLOWED_TRACKS:
            failures.append(f"{system_id or row_label} invalid track: {track}")

        gate_level = str(entry.get("gate_level") or "").strip()
        if gate_level not in ALLOWED_GATE_LEVELS:
            failures.append(f"{system_id or row_label} invalid gate_level: {gate_level}")

        pack = str(entry.get("pack") or "").strip()
        if not pack:
            failures.append(f"{system_id or row_label} missing pack")

        profiles = entry.get("profiles", [])
        if not isinstance(profiles, list) or not profiles:
            failures.append(f"{system_id or row_label} profiles must be a non-empty list")
        else:
            invalid_profiles = sorted({str(value) for value in profiles if str(value) not in ALLOWED_PROFILES})
            if invalid_profiles:
                failures.append(f"{system_id or row_label} invalid profiles: {invalid_profiles}")

        script = str(entry.get("script") or "").strip()
        if not script:
            failures.append(f"{system_id or row_label} script path empty")
        else:
            try:
                if not _repo_path(script).exists():
                    failures.append(f"{system_id or row_label} missing script: {script}")
            except Exception:
                failures.append(f"{system_id or row_label} invalid script path: {script}")

        outputs = entry.get("outputs", [])
        if not isinstance(outputs, list) or not outputs:
            failures.append(f"{system_id or row_label} outputs must be a non-empty list")
        else:
            for out_path in outputs:
                text = str(out_path).strip()
                if not text:
                    failures.append(f"{system_id or row_label} has empty output path")
                    continue
                try:
                    _repo_path(text)
                except Exception:
                    failures.append(f"{system_id or row_label} invalid output path: {text}")

        depends_on = entry.get("depends_on", [])
        if not isinstance(depends_on, list):
            failures.append(f"{system_id or row_label} depends_on must be a list")

        cache_artifacts = entry.get("cache_artifacts", [])
        if not isinstance(cache_artifacts, list):
            failures.append(f"{system_id or row_label} cache_artifacts must be a list")
            cache_artifacts = []
        if mode == "live" and not cache_artifacts:
            failures.append(f"{system_id or row_label} live entries require cache_artifacts")
        for cache_path in cache_artifacts:
            text = str(cache_path).strip()
            if not text:
                failures.append(f"{system_id or row_label} has empty cache_artifact path")
                continue
            try:
                _repo_path(text)
            except Exception:
                failures.append(f"{system_id or row_label} invalid cache_artifact path: {text}")

        timeout_sec = entry.get("timeout_sec")
        if not isinstance(timeout_sec, int) or timeout_sec <= 0:
            failures.append(f"{system_id or row_label} timeout_sec must be a positive integer")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "system_count": len(systems),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped_json = reports_dir / f"{stamp}-trinity-expansion-manifest-validation.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-expansion-manifest-validation.md"
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    for path in (latest_json, latest_md):
        path.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md = _markdown(payload)
    timestamped_md.write_text(md, encoding="utf-8")
    latest_md.write_text(md, encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"effective_success={payload['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    if payload["effective_success"]:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
