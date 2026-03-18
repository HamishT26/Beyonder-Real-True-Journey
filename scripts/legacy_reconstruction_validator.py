#!/usr/bin/env python3
"""Validate the active legacy reconstruction lane."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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


def _markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Legacy Reconstruction Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- reconstructed_modules: `{payload['reconstructed_modules']}`",
        "",
        "## Failures",
    ]
    if payload["failures"]:
        lines.extend(f"- {item}" for item in payload["failures"])
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the active legacy reconstruction lane.")
    parser.add_argument("--legacy-map", default="docs/v29-v38-legacy-reconstruction-map-v1.json")
    parser.add_argument("--latest-json", default="docs/v15-legacy-reconstruction-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/v15-legacy-reconstruction-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    legacy_map_path = _repo_path(args.legacy_map)
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)

    if not legacy_map_path.exists():
        failures.append(f"missing legacy map: {args.legacy_map}")
        payload = {}
    else:
        payload = json.loads(legacy_map_path.read_text(encoding="utf-8"))

    reconstructed = payload.get("reconstructed_modules", []) if isinstance(payload, dict) else []
    if not isinstance(reconstructed, list) or len(reconstructed) != 6:
        failures.append("legacy map must contain exactly six reconstructed modules")
        reconstructed = []

    for row in reconstructed:
        if not isinstance(row, dict):
            failures.append("reconstructed module entry must be an object")
            continue
        script = str(row.get("script") or "").strip()
        if not script:
            failures.append("reconstructed module entry missing script")
            continue
        if not _repo_path(script).exists():
            failures.append(f"missing reconstructed script: {script}")

    payload_out = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "reconstructed_modules": len(reconstructed),
        "failures": failures,
        "warnings": warnings,
    }
    latest_json.write_text(json.dumps(payload_out, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(_markdown(payload_out), encoding="utf-8")
    print(f"legacy_reconstruction_validation={payload_out['overall_status']}")
    if failures or (warnings and args.fail_on_warn):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
