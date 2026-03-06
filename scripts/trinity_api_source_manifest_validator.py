#!/usr/bin/env python3
"""Validate the Trinity public API manifest, query pack, and cache targets."""

from __future__ import annotations

import argparse
from typing import Any
from urllib.parse import urlparse

from trinity_api_common import (
    ALLOWED_PILLARS,
    append_check,
    iso_now,
    load_manifest,
    load_query_pack,
    parse_datetime,
    repo_path,
    save_json_and_markdown_run,
    severity,
)

REQUIRED_API_FIELDS = {
    "api_id",
    "pillar",
    "base_url",
    "auth_mode",
    "format",
    "refresh_script",
    "cache_artifact",
    "refresh_window_days",
    "enabled_by_default",
    "rate_limit_note",
}


def _valid_url(raw: str) -> bool:
    parsed = urlparse(str(raw))
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Trinity API Source Manifest Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- manifest_path: `{payload['manifest_path']}`",
        f"- query_pack_path: `{payload['query_pack_path']}`",
        f"- api_count: `{payload['api_count']}`",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in payload["checks"]:
        lines.append(f"| {check['name']} | {check['status']} | {check['detail']} |")
    lines.extend(
        [
            "",
            "## API roster",
            "| api_id | pillar | cache_artifact | refresh_script | enabled_by_default |",
            "|---|---|---|---|---|",
        ]
    )
    for api in payload["apis"]:
        lines.append(
            f"| {api['api_id']} | {api['pillar']} | `{api['cache_artifact']}` | "
            f"`{api['refresh_script']}` | `{api['enabled_by_default']}` |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Trinity API manifest and cached targets.")
    parser.add_argument("--manifest", default="docs/trinity-api-source-manifest-v1.json")
    parser.add_argument("--query-pack", default="docs/trinity-api-query-pack-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-api-manifest-runs")
    parser.add_argument("--latest-json", default="docs/trinity-api-source-manifest-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-api-source-manifest-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    query_pack = load_query_pack(args.query_pack)
    checks: list[dict[str, Any]] = []
    apis = manifest.get("apis", [])

    header_failures: list[str] = []
    for key in ("generated_utc", "refresh_window_days", "apis"):
        if key not in manifest:
            header_failures.append(f"missing top-level manifest key: {key}")
    if not isinstance(apis, list) or not apis:
        header_failures.append("apis must be a non-empty list")
    try:
        parse_datetime(str(manifest.get("generated_utc")))
    except Exception as exc:  # noqa: BLE001
        header_failures.append(f"invalid manifest generated_utc: {exc}")
    append_check(checks, "manifest_header", header_failures, [])

    api_failures: list[str] = []
    seen_ids: set[str] = set()
    cache_targets: set[str] = set()
    for index, api in enumerate(apis, start=1):
        missing = sorted(REQUIRED_API_FIELDS - set(api))
        if missing:
            api_failures.append(f"api[{index}] missing fields: {', '.join(missing)}")
            continue
        api_id = str(api["api_id"])
        if api_id in seen_ids:
            api_failures.append(f"duplicate api_id: {api_id}")
        seen_ids.add(api_id)
        if str(api["pillar"]) not in ALLOWED_PILLARS:
            api_failures.append(f"api[{index}] invalid pillar: {api['pillar']}")
        if str(api["auth_mode"]) != "public_unauthenticated":
            api_failures.append(f"api[{index}] invalid auth_mode: {api['auth_mode']}")
        if bool(api["enabled_by_default"]):
            api_failures.append(f"api[{index}] enabled_by_default must be false: {api_id}")
        if not _valid_url(str(api["base_url"])):
            api_failures.append(f"api[{index}] invalid base_url: {api['base_url']}")
        try:
            script_path = repo_path(str(api["refresh_script"]))
            if not script_path.exists():
                api_failures.append(f"api[{index}] missing refresh_script: {api['refresh_script']}")
        except Exception as exc:  # noqa: BLE001
            api_failures.append(f"api[{index}] invalid refresh_script {api['refresh_script']}: {exc}")
        try:
            cache_path = repo_path(str(api["cache_artifact"]))
            cache_targets.add(str(api["cache_artifact"]))
            if not cache_path.exists():
                api_failures.append(f"api[{index}] missing cache target: {api['cache_artifact']}")
        except Exception as exc:  # noqa: BLE001
            api_failures.append(f"api[{index}] invalid cache_artifact {api['cache_artifact']}: {exc}")
    append_check(checks, "api_schema", api_failures, [])

    query_failures: list[str] = []
    for pillar in ("mind", "body", "heart"):
        if pillar not in query_pack:
            query_failures.append(f"missing query-pack section: {pillar}")
    if "mind" in query_pack and not query_pack["mind"].get("queries"):
        query_failures.append("mind queries must be non-empty")
    if "body" in query_pack:
        for key in ("crossref_queries", "github_watchlist", "github_search_queries"):
            if not query_pack["body"].get(key):
                query_failures.append(f"body {key} must be non-empty")
    if "heart" in query_pack:
        for key in ("world_bank_indicators", "oecd_keywords", "data_govt_queries"):
            if not query_pack["heart"].get(key):
                query_failures.append(f"heart {key} must be non-empty")
    append_check(checks, "query_pack", query_failures, [])

    coverage_failures: list[str] = []
    expected_cache_targets = {
        "docs/trinity-api-cache/mind-signals-latest.json",
        "docs/trinity-api-cache/body-signals-latest.json",
        "docs/trinity-api-cache/heart-signals-latest.json",
    }
    for path in sorted(expected_cache_targets - cache_targets):
        coverage_failures.append(f"missing required cache target entry: {path}")
    append_check(checks, "cache_target_coverage", coverage_failures, [])

    overall_status = "PASS"
    for check in checks:
        overall_status = max(overall_status, str(check["status"]), key=severity)

    payload = {
        "generated_utc": iso_now(),
        "overall_status": overall_status,
        "manifest_path": args.manifest,
        "query_pack_path": args.query_pack,
        "api_count": len(apis) if isinstance(apis, list) else 0,
        "checks": checks,
        "apis": apis,
        "effective_success": overall_status == "PASS",
    }
    markdown = _build_markdown(payload)
    save_json_and_markdown_run(
        payload=payload,
        markdown=markdown,
        latest_json=args.latest_json,
        latest_md=args.latest_md,
        reports_dir=args.reports_dir,
        stem="trinity-api-source-manifest-validation",
    )
    print(f"overall_status={overall_status}")
    print(f"api_count={payload['api_count']}")
    if args.fail_on_warn and overall_status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
