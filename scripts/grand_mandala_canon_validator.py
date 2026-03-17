#!/usr/bin/env python3
"""Validate the canonical GMUT surface for the current Trinity phase."""

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
        "# GMUT Canon Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        "",
        "## Failures",
    ]
    if payload["failures"]:
        lines.extend(f"- {item}" for item in payload["failures"])
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings"])
    if payload["warnings"]:
        lines.extend(f"- {item}" for item in payload["warnings"])
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the canonical GMUT surface.")
    parser.add_argument("--tex", default="latex/grand_mandala.tex")
    parser.add_argument("--registry", default="docs/grand-mandala-equation-registry-v1.json")
    parser.add_argument("--latest-json", default="docs/v14-gmut-canon-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/v14-gmut-canon-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    tex_path = _repo_path(args.tex)
    registry_path = _repo_path(args.registry)
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)

    if not tex_path.exists():
        failures.append(f"missing canonical tex: {args.tex}")
        tex_text = ""
    else:
        tex_text = tex_path.read_text(encoding="utf-8")

    if not registry_path.exists():
        failures.append(f"missing equation registry: {args.registry}")
        registry = {}
    else:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))

    required_tex_tokens = [
        "Grand Mandala Unified Theory v13 Canonical Surface",
        "\\mathcal{G}_{AB}",
        "\\mathcal{L}_{\\mathrm{GMUT},v13}",
        "confirmed\\_evidence",
        "open\\_gap",
    ]
    for token in required_tex_tokens:
        if token not in tex_text:
            failures.append(f"tex missing token: {token}")

    equations = registry.get("equations", []) if isinstance(registry, dict) else []
    if not isinstance(equations, list) or len(equations) < 2:
        failures.append("registry requires at least two canonical equation entries")

    terms = registry.get("terms", []) if isinstance(registry, dict) else []
    if not isinstance(terms, list) or not any(str(row.get("evidence_posture")) == "open_gap" for row in terms if isinstance(row, dict)):
        failures.append("registry terms must include at least one open_gap entry")

    if isinstance(registry, dict) and str(registry.get("canonical_surface")) != args.tex:
        failures.append("registry canonical_surface does not match tex path")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "failures": failures,
        "warnings": warnings,
        "canonical_surface": args.tex,
        "registry": args.registry,
    }
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(_markdown(payload), encoding="utf-8")
    print(f"gmut_canon_validation={payload['overall_status']}")
    if failures or (warnings and args.fail_on_warn):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
