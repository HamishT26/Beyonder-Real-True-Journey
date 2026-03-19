#!/usr/bin/env python3
"""Validate the v17 standards-backed bridge registry."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_DOMAIN_SNIPPETS = (
    "nist.gov",
    "csrc.nist.gov",
    "modelcontextprotocol.io",
    "digital-strategy.ec.europa.eu",
    "w3.org",
    "openid.net",
    "spec.c2pa.org",
    "mlcommons.org",
    "docs.mlcommons.org",
    "fda.gov",
    "who.int",
    "unesco.org",
)


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path_str: str) -> dict[str, Any]:
    return json.loads(_repo_path(path_str).read_text(encoding="utf-8"))


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V17 Standards Bridge Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- source_count: `{payload['source_count']}`",
        "",
        "## Failures",
    ]
    lines.extend([f"- {item}" for item in payload["failures"]] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in payload["warnings"]] or ["- none"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the v17 standards bridge registry.")
    parser.add_argument("--registry", default="docs/v17-standards-bridge-registry-v1.json")
    parser.add_argument("--reports-dir", default="docs/v17-standards-bridge-runs")
    parser.add_argument("--latest-json", default="docs/v17-standards-bridge-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/v17-standards-bridge-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    registry = _read_json(args.registry)
    claim_boundaries = registry.get("claim_boundaries", [])
    if not isinstance(claim_boundaries, list):
        claim_boundaries = []
    top_level_boundary_text = " ".join(str(item) for item in claim_boundaries if str(item).strip())
    registry_notes_target = str(registry.get("notes_target") or "").strip()
    allowed_source_tiers = {
        str(item).strip()
        for item in registry.get("allowed_source_tiers", [])
        if str(item).strip()
    }

    collection_key = "sources"
    sources = registry.get("sources", [])
    if not isinstance(sources, list) or not sources:
        collection_key = "inputs"
        sources = registry.get("inputs", [])
    if not isinstance(sources, list) or not sources:
        failures.append("registry must expose a non-empty sources or inputs list")
        sources = []

    for index, row in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(row, dict):
            failures.append(f"{label} must be an object")
            continue
        if collection_key == "sources":
            for field in ("lane_id", "category", "source_name", "source_url", "fit_surfaces", "claim_boundary", "risk_note"):
                if field not in row:
                    failures.append(f"{label} missing field: {field}")
            source_url = str(row.get("source_url") or "").strip()
            fit_ok = isinstance(row.get("fit_surfaces"), list) and bool(row.get("fit_surfaces"))
            boundary_text = str(row.get("claim_boundary") or "").strip()
            risk_text = str(row.get("risk_note") or "").strip()
            category_text = str(row.get("category") or "").strip()
            name_text = str(row.get("source_name") or "").strip()
        else:
            for field in ("id", "input_class", "publisher", "title", "url", "why_it_matters", "allowed_repo_use", "disallowed_repo_use"):
                if field not in row:
                    failures.append(f"{label} missing field: {field}")
            source_url = str(row.get("url") or "").strip()
            fit_ok = bool(str(row.get("allowed_repo_use") or "").strip())
            boundary_text = " ".join(
                part
                for part in (
                    top_level_boundary_text,
                    str(row.get("disallowed_repo_use") or "").strip(),
                )
                if part
            )
            risk_text = str(row.get("why_it_matters") or "").strip()
            category_text = str(row.get("input_class") or "").strip()
            name_text = str(row.get("title") or "").strip()
            notes_target = str(row.get("notes_target") or "").strip()
            disallowed_repo_use = str(row.get("disallowed_repo_use") or "").strip()
            allowed_input_classes = registry.get("allowed_input_classes", [])
            if isinstance(allowed_input_classes, list) and allowed_input_classes and category_text not in {str(item) for item in allowed_input_classes}:
                failures.append(f"{label} input_class must be one of allowed_input_classes")
            source_tier = str(row.get("source_tier") or "").strip()
            if allowed_source_tiers and source_tier not in allowed_source_tiers:
                failures.append(f"{label} source_tier must be one of allowed_source_tiers")
            if not notes_target:
                failures.append(f"{label} notes_target must be non-empty")
            elif registry_notes_target and not notes_target.startswith(registry_notes_target):
                failures.append(f"{label} notes_target must stay under the registry notes_target surface")
            if not disallowed_repo_use:
                failures.append(f"{label} disallowed_repo_use must be non-empty")
        if not source_url:
            failures.append(f"{label} source_url must be non-empty")
        else:
            parsed = urlparse(source_url)
            if parsed.scheme != "https":
                failures.append(f"{label} source_url must use https")
            domain = parsed.netloc.lower()
            if not any(snippet in domain for snippet in ALLOWED_DOMAIN_SNIPPETS):
                failures.append(f"{label} source_url must be on an approved official domain")
        if not name_text:
            failures.append(f"{label} source_name must be non-empty")
        if not category_text:
            failures.append(f"{label} category must be non-empty")
        if not fit_ok:
            failures.append(f"{label} fit_surfaces or allowed_repo_use must be non-empty")
        if not boundary_text:
            failures.append(f"{label} claim_boundary must be non-empty")
        elif "not externally establish" not in boundary_text.lower() and "not external proof" not in boundary_text.lower():
            warnings.append(f"{label} claim_boundary should explicitly note that the source does not externally establish GMUT, Trinity Hybrid OS, or Freed ID/Cosmic Bill")
        if not risk_text:
            failures.append(f"{label} risk_note must be non-empty")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "source_count": len(sources),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    (reports_dir / f"{stamp}-v17-standards-bridge-validation.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (reports_dir / f"{stamp}-v17-standards-bridge-validation.md").write_text(_markdown(payload), encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(_markdown(payload), encoding="utf-8")
    print(f"overall_status={payload['overall_status']}")
    print(f"effective_success={payload['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
