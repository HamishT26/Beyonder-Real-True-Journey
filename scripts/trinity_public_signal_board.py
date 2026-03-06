#!/usr/bin/env python3
"""Emit a cached public-signal board for Mind, Body, and Heart."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
TIER_RANK = {
    "official_primary": 0,
    "research_primary": 1,
    "official_secondary": 2,
    "public_reporting": 3,
}


@dataclass
class ArtifactStatus:
    label: str
    path: str
    status: str
    detail: str


def _repo_path(path: str) -> Path:
    resolved = (ROOT / path).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(raw: object) -> str:
    text = str(raw or "").strip().upper()
    if text in {"PASS", "WARN", "FAIL", "TIMEOUT"}:
        return text
    return "FAIL"


def _severity(status: str) -> int:
    return {"PASS": 0, "WARN": 1, "FAIL": 2, "TIMEOUT": 3}.get(status, 2)


def _extract_status(path: str, payload: dict[str, object]) -> str:
    if path == "docs/mind-track-gmut-anchor-exclusion-latest.json":
        comparator_status = _normalize_status(payload.get("comparator_status"))
        missing_fields = int(payload.get("anchors_with_missing_required_fields", 0) or 0)
        if comparator_status == "PASS" and missing_fields == 0:
            return "PASS"

    if isinstance(payload.get("effective_success"), bool):
        return "PASS" if payload["effective_success"] else "FAIL"
    if "overall_status" in payload:
        return _normalize_status(payload["overall_status"])
    if "status" in payload:
        return _normalize_status(payload["status"])
    return "FAIL"


def _extract_detail(payload: dict[str, object]) -> str:
    counts = payload.get("counts")
    if isinstance(counts, dict):
        return (
            f"pass={counts.get('pass', 0)}, warn={counts.get('warn', 0)}, fail={counts.get('fail', 0)}"
        )

    summary = payload.get("summary")
    if isinstance(summary, dict):
        parts: list[str] = []
        for key in ("pass_rate", "body_health_score", "benchmark_status", "total_duration_seconds"):
            if key in summary:
                parts.append(f"{key}={summary[key]}")
        if parts:
            return ", ".join(parts)

    trend = payload.get("trend_classification")
    if trend:
        return f"trend={trend}"

    final_case = payload.get("final_case")
    if isinstance(final_case, dict) and "status" in final_case:
        return f"final_case_status={final_case['status']}"

    checks = payload.get("checks")
    if isinstance(checks, list):
        passed = sum(
            1
            for check in checks
            if isinstance(check, dict) and _normalize_status(check.get("status")) == "PASS"
        )
        return f"checks={passed}/{len(checks)}"

    return "status extracted"


def _artifact_status(label: str, path: str) -> ArtifactStatus:
    file_path = _repo_path(path)
    if not file_path.exists():
        return ArtifactStatus(label=label, path=path, status="FAIL", detail="missing artifact")
    payload = _read_json(file_path)
    return ArtifactStatus(
        label=label,
        path=path,
        status=_extract_status(path, payload),
        detail=_extract_detail(payload),
    )


def _parse_datetime(raw: str) -> datetime:
    normalized = raw.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _parse_date(raw: str) -> date:
    return date.fromisoformat(raw)


def _freshness_status(
    *,
    registry_generated_utc: datetime,
    refresh_window_days: int,
    latest_source_date: date,
    fresh_source_days: int,
    aging_source_days: int,
) -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    registry_age_days = max((now - registry_generated_utc).days, 0)
    source_age_days = max((now.date() - latest_source_date).days, 0)
    if registry_age_days > refresh_window_days or source_age_days > aging_source_days:
        return (
            "FAIL",
            f"registry_age_days={registry_age_days}, latest_source_age_days={source_age_days}",
        )
    if source_age_days > fresh_source_days:
        return (
            "WARN",
            f"latest_source_age_days={source_age_days} exceeds fresh window {fresh_source_days}",
        )
    return (
        "PASS",
        f"registry_age_days={registry_age_days}, latest_source_age_days={source_age_days}",
    )


def _pillar_artifacts(pillar: str) -> list[ArtifactStatus]:
    if pillar == "mind":
        return [
            _artifact_status("GMUT comparator", "docs/mind-track-gmut-comparator-latest.json"),
            _artifact_status("Anchor exclusion note", "docs/mind-track-gmut-anchor-exclusion-latest.json"),
            _artifact_status("Anchor trace validation", "docs/mind-track-gmut-trace-validation-latest.json"),
        ]
    if pillar == "body":
        return [
            _artifact_status("Body smoke", "docs/body-track-smoke-latest.json"),
            _artifact_status("Benchmark guardrail", "docs/body-track-benchmark-latest.json"),
            _artifact_status("Trend guard", "docs/body-track-trend-guard-latest.json"),
            _artifact_status("Stress window", "docs/body-track-policy-stress-latest.json"),
        ]
    return [
        _artifact_status("Minimum disclosure", "docs/heart-track-min-disclosure-latest.json"),
        _artifact_status("Minimum disclosure adversarial", "docs/heart-track-min-disclosure-adversarial-latest.json"),
        _artifact_status("Minimum disclosure live path", "docs/heart-track-min-disclosure-live-latest.json"),
        _artifact_status("Dispute recourse", "docs/heart-track-dispute-recourse-latest.json"),
        _artifact_status("Dispute recourse adversarial", "docs/heart-track-dispute-recourse-adversarial-latest.json"),
    ]


def _repo_validation_status(rows: Iterable[ArtifactStatus]) -> tuple[str, list[dict[str, object]], list[str]]:
    artifacts = list(rows)
    status = "PASS"
    failing: list[str] = []
    for artifact in artifacts:
        if _severity(artifact.status) > _severity(status):
            status = artifact.status
        if artifact.status != "PASS":
            failing.append(artifact.label)
    return status, [asdict(artifact) for artifact in artifacts], failing


def _highest_tier_sources(sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rank = min(TIER_RANK.get(str(source["source_tier"]), 9) for source in sources)
    chosen = [
        {
            "publisher": source["publisher"],
            "topic": source["topic"],
            "source_tier": source["source_tier"],
            "published_at": source["published_at"],
            "url": source["url"],
        }
        for source in sources
        if TIER_RANK.get(str(source["source_tier"]), 9) == rank
    ]
    chosen.sort(key=lambda item: (item["published_at"], item["publisher"], item["topic"]), reverse=True)
    return chosen


def _build_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Trinity Public Signal Board",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- registry_validation_status: `{payload['registry_validation_status']}`",
        "",
        "## Pillar board",
        "| pillar | status | freshness_status | source_count | repo_validation_status | next_refresh_action |",
        "|---|---|---|---|---|---|",
    ]
    for pillar in ("mind", "body", "heart"):
        row = payload["pillars"][pillar]
        lines.append(
            f"| {pillar} | {row['status']} | {row['freshness_status']} | {row['source_count']} | "
            f"{row['repo_validation_status']} | {row['next_refresh_action']} |"
        )

    for pillar in ("mind", "body", "heart"):
        row = payload["pillars"][pillar]
        lines.extend(
            [
                "",
                f"## {pillar.title()} detail",
                f"- freshness_status: `{row['freshness_status']}`",
                f"- freshness_detail: `{row['freshness_detail']}`",
                f"- source_count: `{row['source_count']}`",
                f"- repo_validation_status: `{row['repo_validation_status']}`",
                f"- repo_targets_touched: `{', '.join(row['repo_targets_touched'])}`",
                "",
                "### Highest-tier sources",
                "| publisher | topic | tier | published_at | url |",
                "|---|---|---|---|---|",
            ]
        )
        for source in row["highest_tier_sources"]:
            lines.append(
                f"| {source['publisher']} | {source['topic']} | {source['source_tier']} | "
                f"{source['published_at']} | `{source['url']}` |"
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit a cached public signal board for Trinity research.")
    parser.add_argument("--registry", default="docs/trinity-public-source-registry-v1.json")
    parser.add_argument("--validator-json", default="docs/trinity-public-research-validation-latest.json")
    parser.add_argument("--reports-dir", default="docs/trinity-public-signal-runs")
    parser.add_argument("--latest-json", default="docs/trinity-public-signal-board-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-public-signal-board-latest.md")
    parser.add_argument("--fresh-source-days", type=int, default=365)
    parser.add_argument("--aging-source-days", type=int, default=730)
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    registry = _read_json(_repo_path(args.registry))
    validator = _read_json(_repo_path(args.validator_json))
    reports_dir = _repo_path(args.reports_dir)
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    registry_generated_utc = _parse_datetime(str(registry["generated_utc"]))
    refresh_window_days = int(registry["refresh_window_days"])
    registry_validation_status = _normalize_status(validator.get("overall_status"))

    grouped_sources: dict[str, list[dict[str, object]]] = {"mind": [], "body": [], "heart": []}
    for source in registry["sources"]:
        grouped_sources[str(source["pillar"])].append(source)

    pillars: dict[str, dict[str, object]] = {}
    overall_status = registry_validation_status
    for pillar in ("mind", "body", "heart"):
        sources = grouped_sources[pillar]
        latest_source_date = max(_parse_date(str(source["published_at"])) for source in sources)
        freshness_status, freshness_detail = _freshness_status(
            registry_generated_utc=registry_generated_utc,
            refresh_window_days=refresh_window_days,
            latest_source_date=latest_source_date,
            fresh_source_days=args.fresh_source_days,
            aging_source_days=args.aging_source_days,
        )
        repo_validation_status, artifacts, failing = _repo_validation_status(_pillar_artifacts(pillar))
        targets = sorted(
            {
                str(target)
                for source in sources
                for target in source["repo_relevance"]["targets"]
            }
        )
        status = max(freshness_status, repo_validation_status, key=_severity)
        overall_status = max(overall_status, status, key=_severity)
        next_refresh_action = (
            f"Refresh cached {pillar} sources and rerun the validator."
            if freshness_status != "PASS"
            else (
                f"Investigate repo validation drift in {', '.join(failing)} before updating comparison docs."
                if repo_validation_status != "PASS"
                else f"Refresh when a newer high-tier {pillar} source lands or when one of the target docs changes."
            )
        )
        pillars[pillar] = {
            "status": status,
            "freshness_status": freshness_status,
            "freshness_detail": freshness_detail,
            "latest_publication_at": latest_source_date.isoformat(),
            "source_count": len(sources),
            "highest_tier_sources": _highest_tier_sources(sources),
            "repo_targets_touched": targets,
            "repo_validation_status": repo_validation_status,
            "repo_validation_artifacts": artifacts,
            "watch_items": failing,
            "next_refresh_action": next_refresh_action,
        }

    payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "registry_validation_status": registry_validation_status,
        "registry_generated_utc": registry_generated_utc.isoformat(),
        "refresh_window_days": refresh_window_days,
        "pillars": pillars,
        "evidence_boundary": {
            "research_layer": "This board is a cached public-source intelligence layer.",
            "runtime_layer": "Runtime readiness remains governed by the deterministic suite and mandala scoreboard.",
            "promotion_rule": "Use public-source refreshes to refine comparison language and next checks, not to bypass measured repo evidence.",
        },
    }
    markdown = _build_markdown(payload)

    timestamped_json = reports_dir / f"{stamp}-trinity-public-signal-board.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-public-signal-board.md"
    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
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
