#!/usr/bin/env python3
"""Validate cached Trinity public research artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_PILLARS = {"mind", "body", "heart"}
ALLOWED_TIERS = {"official_primary", "official_secondary", "research_primary", "public_reporting"}
COMPARISON_TIERS = {"official_primary", "official_secondary", "research_primary"}
REQUIRED_FIELDS = {
    "pillar",
    "topic",
    "publisher",
    "url",
    "published_at",
    "jurisdiction",
    "source_tier",
    "source_kind",
    "summary",
    "repo_relevance",
    "next_validation_target",
}


def _normalize_status(raw: str) -> str:
    text = str(raw or "").strip().upper()
    if text in {"PASS", "WARN", "FAIL"}:
        return text
    return "FAIL"


def _severity(status: str) -> int:
    return {"PASS": 0, "WARN": 1, "FAIL": 2}.get(status, 2)


def _repo_path(path: str) -> Path:
    resolved = (ROOT / path).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _parse_datetime(raw: str) -> datetime:
    normalized = raw.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _parse_date(raw: str) -> date:
    return date.fromisoformat(raw)


def _check_url(raw: str) -> bool:
    parsed = urlparse(raw)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _status_for_failures(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _append_check(checks: list[dict[str, object]], name: str, failures: list[str], warnings: list[str]) -> None:
    status = _status_for_failures(failures, warnings)
    detail_parts: list[str] = []
    if failures:
        detail_parts.append("; ".join(failures))
    if warnings:
        detail_parts.append("; ".join(warnings))
    checks.append(
        {
            "name": name,
            "status": status,
            "detail": " | ".join(detail_parts) if detail_parts else "ok",
        }
    )


def _build_markdown(payload: dict[str, object]) -> str:
    counts = payload["counts"]
    lines = [
        "# Trinity Public Research Validation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- registry_path: `{payload['registry_path']}`",
        f"- registry_generated_utc: `{payload['registry_generated_utc']}`",
        f"- registry_age_days: `{payload['registry_age_days']}`",
        f"- refresh_window_days: `{payload['refresh_window_days']}`",
        f"- pass: `{counts['pass']}`",
        f"- warn: `{counts['warn']}`",
        f"- fail: `{counts['fail']}`",
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
            "## Pillar counts",
            "| pillar | source_count |",
            "|---|---|",
        ]
    )
    for pillar, count in payload["pillar_source_counts"].items():
        lines.append(f"| {pillar} | {count} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cached Trinity public-source research artifacts.")
    parser.add_argument("--registry", default="docs/trinity-public-source-registry-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-public-research-runs")
    parser.add_argument("--latest-json", default="docs/trinity-public-research-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-public-research-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    registry_path = _repo_path(args.registry)
    reports_dir = _repo_path(args.reports_dir)
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)

    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    checks: list[dict[str, object]] = []
    pillar_counts = {pillar: 0 for pillar in sorted(ALLOWED_PILLARS)}
    registry_generated_utc = ""
    registry_age_days = -1
    refresh_window_days = 0

    if not registry_path.exists():
        payload = {
            "generated_utc": generated_utc,
            "overall_status": "FAIL",
            "registry_path": str(Path(args.registry).as_posix()),
            "registry_generated_utc": None,
            "registry_age_days": None,
            "refresh_window_days": None,
            "pillar_source_counts": pillar_counts,
            "counts": {"pass": 0, "warn": 0, "fail": 1},
            "checks": [{"name": "registry_exists", "status": "FAIL", "detail": "missing registry file"}],
            "effective_success": False,
        }
        markdown = _build_markdown(payload)
        (reports_dir / f"{stamp}-trinity-public-research-validation.json").write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
        (reports_dir / f"{stamp}-trinity-public-research-validation.md").write_text(markdown, encoding="utf-8")
        latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        latest_md.write_text(markdown, encoding="utf-8")
        print("overall_status=FAIL")
        print("detail=missing registry file")
        return 1

    payload = json.loads(registry_path.read_text(encoding="utf-8"))

    header_failures: list[str] = []
    header_warnings: list[str] = []
    for key in ("generated_utc", "refresh_window_days", "sources"):
        if key not in payload:
            header_failures.append(f"missing top-level key: {key}")
    if not isinstance(payload.get("sources"), list) or not payload.get("sources"):
        header_failures.append("sources must be a non-empty list")
    try:
        registry_generated = _parse_datetime(str(payload.get("generated_utc")))
        registry_generated_utc = registry_generated.isoformat()
    except Exception as exc:  # noqa: BLE001
        header_failures.append(f"invalid generated_utc: {exc}")
        registry_generated = datetime.now(timezone.utc)
        registry_generated_utc = str(payload.get("generated_utc"))

    try:
        refresh_window_days = int(payload.get("refresh_window_days"))
        if refresh_window_days <= 0:
            raise ValueError("must be > 0")
    except Exception as exc:  # noqa: BLE001
        header_failures.append(f"invalid refresh_window_days: {exc}")
        refresh_window_days = 0

    if not header_failures and refresh_window_days > 0:
        registry_age_days = max((datetime.now(timezone.utc) - registry_generated).days, 0)
        if registry_age_days > refresh_window_days:
            header_warnings.append(
                f"registry age {registry_age_days}d exceeds refresh window {refresh_window_days}d"
            )

    _append_check(checks, "registry_header", header_failures, header_warnings)

    source_failures: list[str] = []
    source_warnings: list[str] = []
    comparison_tier_counts = {pillar: 0 for pillar in sorted(ALLOWED_PILLARS)}
    for index, source in enumerate(payload.get("sources", []), start=1):
        missing = sorted(REQUIRED_FIELDS - set(source))
        if missing:
            source_failures.append(f"source[{index}] missing fields: {', '.join(missing)}")
            continue

        pillar = source["pillar"]
        if pillar not in ALLOWED_PILLARS:
            source_failures.append(f"source[{index}] invalid pillar: {pillar}")
        else:
            pillar_counts[pillar] += 1

        tier = source["source_tier"]
        if tier not in ALLOWED_TIERS:
            source_failures.append(f"source[{index}] invalid source_tier: {tier}")
        elif pillar in comparison_tier_counts and tier in COMPARISON_TIERS:
            comparison_tier_counts[pillar] += 1

        if not _check_url(str(source["url"])):
            source_failures.append(f"source[{index}] invalid url: {source['url']}")
        try:
            _parse_date(str(source["published_at"]))
        except Exception as exc:  # noqa: BLE001
            source_failures.append(f"source[{index}] invalid published_at: {exc}")

        repo_relevance = source["repo_relevance"]
        if not isinstance(repo_relevance, dict):
            source_failures.append(f"source[{index}] repo_relevance must be an object")
        else:
            targets = repo_relevance.get("targets")
            if not isinstance(targets, list) or not targets:
                source_failures.append(f"source[{index}] repo_relevance.targets must be a non-empty list")
            else:
                for target in targets:
                    try:
                        if not _repo_path(str(target)).exists():
                            source_failures.append(f"source[{index}] missing repo target: {target}")
                    except Exception as exc:  # noqa: BLE001
                        source_failures.append(f"source[{index}] invalid repo target {target}: {exc}")

        next_target = source["next_validation_target"]
        if not isinstance(next_target, dict):
            source_failures.append(f"source[{index}] next_validation_target must be an object")
        else:
            target = next_target.get("target")
            action = next_target.get("action")
            if not target or not action:
                source_failures.append(
                    f"source[{index}] next_validation_target requires target and action"
                )
            else:
                try:
                    if not _repo_path(str(target)).exists():
                        source_failures.append(f"source[{index}] missing next validation target: {target}")
                except Exception as exc:  # noqa: BLE001
                    source_failures.append(f"source[{index}] invalid next validation target {target}: {exc}")

    for pillar, count in pillar_counts.items():
        if count == 0:
            source_failures.append(f"no sources present for pillar: {pillar}")
    for pillar, count in comparison_tier_counts.items():
        if count == 0:
            source_warnings.append(f"no comparison-eligible sources present for pillar: {pillar}")

    _append_check(checks, "source_schema", source_failures, source_warnings)

    tier_failures: list[str] = []
    tier_warnings: list[str] = []
    for index, source in enumerate(payload.get("sources", []), start=1):
        if str(source.get("source_tier")) != "public_reporting":
            continue
        targets = source.get("repo_relevance", {}).get("targets", [])
        if any(
            str(target)
            in {
                "docs/comparative-validation-grid-v1.md",
                "docs/grand-unified-narrative-brief.md",
                "docs/trinity-public-research-brief-2026-03-06.md",
            }
            for target in targets
        ):
            tier_warnings.append(f"source[{index}] uses public_reporting for comparison-facing targets")
    _append_check(checks, "source_tier_policy", tier_failures, tier_warnings)

    overall_status = "PASS"
    for check in checks:
        overall_status = max(overall_status, _normalize_status(str(check["status"])), key=_severity)

    counts = {
        "pass": sum(1 for check in checks if check["status"] == "PASS"),
        "warn": sum(1 for check in checks if check["status"] == "WARN"),
        "fail": sum(1 for check in checks if check["status"] == "FAIL"),
    }
    result = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "registry_path": str(Path(args.registry).as_posix()),
        "registry_generated_utc": registry_generated_utc,
        "registry_age_days": registry_age_days,
        "refresh_window_days": refresh_window_days,
        "pillar_source_counts": pillar_counts,
        "counts": counts,
        "checks": checks,
        "effective_success": overall_status == "PASS",
    }

    markdown = _build_markdown(result)
    timestamped_json = reports_dir / f"{stamp}-trinity-public-research-validation.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-public-research-validation.md"
    timestamped_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json.relative_to(ROOT)}")
    print(f"timestamped_md={timestamped_md.relative_to(ROOT)}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")

    if overall_status == "FAIL":
        return 1
    if args.fail_on_warn and overall_status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
