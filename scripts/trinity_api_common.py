#!/usr/bin/env python3
"""Shared helpers for the Trinity public API signal layer."""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = "docs/trinity-api-source-manifest-v1.json"
DEFAULT_QUERY_PACK = "docs/trinity-api-query-pack-v1.json"
USER_AGENT = "BeyonderRealTrueJourney/1.0 (+public-signal-layer)"
ALLOWED_PILLARS = {"mind", "body", "heart"}
ALLOWED_STATUSES = {"PASS", "WARN", "FAIL", "TIMEOUT"}
REQUIRED_RECORD_FIELDS = {
    "source_id",
    "record_id",
    "signal_type",
    "title",
    "published_at",
    "source_url",
    "summary",
    "metrics",
    "tags",
    "repo_relevance",
}
HTML_TAG_RE = re.compile(r"<[^>]+>")


def repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def read_json(path: str | Path) -> dict[str, Any]:
    file_path = repo_path(path) if isinstance(path, str) else path
    return json.loads(file_path.read_text(encoding="utf-8"))


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    file_path = repo_path(path) if isinstance(path, str) else path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    file_path = repo_path(path) if isinstance(path, str) else path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso_now() -> str:
    return now_utc().isoformat()


def timestamp_slug() -> str:
    return now_utc().strftime("%Y%m%dT%H%M%SZ")


def parse_datetime(raw: str) -> datetime:
    normalized = str(raw).replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def normalize_status(raw: object) -> str:
    text = str(raw or "").strip().upper()
    if text in ALLOWED_STATUSES:
        return text
    if text in {"OK", "SUCCESS"}:
        return "PASS"
    return "FAIL"


def severity(status: str) -> int:
    return {"PASS": 0, "WARN": 1, "FAIL": 2, "TIMEOUT": 3}.get(status, 2)


def status_from_failures(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def append_check(checks: list[dict[str, object]], name: str, failures: list[str], warnings: list[str]) -> None:
    detail_parts: list[str] = []
    if failures:
        detail_parts.append("; ".join(failures))
    if warnings:
        detail_parts.append("; ".join(warnings))
    checks.append(
        {
            "name": name,
            "status": status_from_failures(failures, warnings),
            "detail": " | ".join(detail_parts) if detail_parts else "ok",
        }
    )


def fetch_text(url: str, *, accept: str | None = None, timeout_sec: int = 30) -> str:
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout_sec) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def fetch_json(url: str, *, accept: str | None = "application/json", timeout_sec: int = 30) -> dict[str, Any] | list[Any]:
    return json.loads(fetch_text(url, accept=accept, timeout_sec=timeout_sec))


def compact_text(raw: str, limit: int = 280) -> str:
    text = " ".join(str(raw or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def strip_html(raw: str) -> str:
    return compact_text(HTML_TAG_RE.sub(" ", str(raw or "")))


def pick_date(value: str | None, fallback: str = "1970-01-01") -> str:
    if not value:
        return fallback
    return str(value)[:10]


def date_from_parts(parts: list[Any] | None, fallback: str = "1970-01-01") -> str:
    if not parts:
        return fallback
    row = parts[0] if isinstance(parts[0], list) else parts
    year = int(row[0]) if len(row) > 0 and row[0] is not None else 1970
    month = int(row[1]) if len(row) > 1 and row[1] is not None else 1
    day = int(row[2]) if len(row) > 2 and row[2] is not None else 1
    return f"{year:04d}-{month:02d}-{day:02d}"


def load_manifest(path: str = DEFAULT_MANIFEST) -> dict[str, Any]:
    return read_json(path)


def load_query_pack(path: str = DEFAULT_QUERY_PACK) -> dict[str, Any]:
    return read_json(path)


def manifest_entry(manifest: dict[str, Any], api_id: str) -> dict[str, Any]:
    for entry in manifest.get("apis", []):
        if str(entry.get("api_id")) == api_id:
            return entry
    raise KeyError(f"Unknown api_id: {api_id}")


def manifest_entries_for_pillar(manifest: dict[str, Any], pillar: str) -> list[dict[str, Any]]:
    return [entry for entry in manifest.get("apis", []) if str(entry.get("pillar")) == pillar]


def sort_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda row: (
            str(row.get("published_at", "")),
            str(row.get("source_id", "")),
            str(row.get("title", "")),
            str(row.get("record_id", "")),
        ),
        reverse=True,
    )


def aggregate_candidate_targets(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    table: dict[str, dict[str, Any]] = {}
    for record in records:
        repo_relevance = record.get("repo_relevance", {})
        targets = repo_relevance.get("targets", []) if isinstance(repo_relevance, dict) else []
        summary = repo_relevance.get("summary", "") if isinstance(repo_relevance, dict) else ""
        for target in targets:
            target_str = str(target)
            bucket = table.setdefault(
                target_str,
                {
                    "target": target_str,
                    "supporting_source_ids": set(),
                    "record_count": 0,
                    "latest_published_at": "1970-01-01",
                    "reason": summary,
                },
            )
            bucket["supporting_source_ids"].add(str(record.get("source_id")))
            bucket["record_count"] = int(bucket["record_count"]) + 1
            if str(record.get("published_at", "")) > str(bucket["latest_published_at"]):
                bucket["latest_published_at"] = str(record.get("published_at"))
            if summary and not bucket["reason"]:
                bucket["reason"] = summary

    rows: list[dict[str, Any]] = []
    for target in sorted(table):
        row = table[target]
        rows.append(
            {
                "target": row["target"],
                "supporting_source_ids": sorted(row["supporting_source_ids"]),
                "record_count": row["record_count"],
                "latest_published_at": row["latest_published_at"],
                "reason": row["reason"],
            }
        )
    rows.sort(key=lambda row: (row["record_count"], row["latest_published_at"], row["target"]), reverse=True)
    return rows


def save_json_run(
    *,
    payload: dict[str, Any],
    latest_json: str,
    reports_dir: str,
    stem: str,
) -> tuple[Path, Path]:
    latest_json_path = repo_path(latest_json)
    reports_dir_path = repo_path(reports_dir)
    reports_dir_path.mkdir(parents=True, exist_ok=True)
    latest_json_path.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json = reports_dir_path / f"{timestamp_slug()}-{stem}.json"
    write_json(timestamped_json, payload)
    write_json(latest_json_path, payload)
    return timestamped_json, latest_json_path


def save_json_and_markdown_run(
    *,
    payload: dict[str, Any],
    markdown: str,
    latest_json: str,
    latest_md: str,
    reports_dir: str,
    stem: str,
) -> tuple[Path, Path, Path, Path]:
    latest_json_path = repo_path(latest_json)
    latest_md_path = repo_path(latest_md)
    reports_dir_path = repo_path(reports_dir)
    reports_dir_path.mkdir(parents=True, exist_ok=True)
    latest_json_path.parent.mkdir(parents=True, exist_ok=True)
    latest_md_path.parent.mkdir(parents=True, exist_ok=True)
    slug = timestamp_slug()
    timestamped_json = reports_dir_path / f"{slug}-{stem}.json"
    timestamped_md = reports_dir_path / f"{slug}-{stem}.md"
    write_json(timestamped_json, payload)
    write_text(timestamped_md, markdown)
    write_json(latest_json_path, payload)
    write_text(latest_md_path, markdown)
    return timestamped_json, timestamped_md, latest_json_path, latest_md_path


def board_from_cache(
    *,
    pillar: str,
    cache_path: str,
    latest_json: str,
    latest_md: str,
    reports_dir: str,
    board_title: str,
    fail_on_warn: bool,
) -> int:
    generated_utc = iso_now()
    cache_file = repo_path(cache_path)
    failures: list[str] = []
    warnings: list[str] = []
    payload: dict[str, Any]

    if not cache_file.exists():
        payload = {
            "generated_utc": generated_utc,
            "overall_status": "FAIL",
            "freshness_status": "FAIL",
            "pillar": pillar,
            "cache_path": cache_path,
            "source_count": 0,
            "apis_checked": [],
            "repo_targets_touched": [],
            "next_refresh_action": f"Run the {pillar} API refresh before relying on this board.",
            "checks": [{"name": "cache_exists", "status": "FAIL", "detail": "missing cache artifact"}],
            "promotion_candidates": [],
            "effective_success": False,
        }
        markdown = render_board_markdown(board_title, payload)
        save_json_and_markdown_run(
            payload=payload,
            markdown=markdown,
            latest_json=latest_json,
            latest_md=latest_md,
            reports_dir=reports_dir,
            stem=f"{pillar}-signal-board",
        )
        print("overall_status=FAIL")
        print(f"latest_json={latest_json}")
        print(f"latest_md={latest_md}")
        return 1

    cache = read_json(cache_file)
    checks: list[dict[str, Any]] = []

    header_failures: list[str] = []
    header_warnings: list[str] = []
    for key in ("generated_utc", "pillar", "refresh_window_days", "source_runs", "records", "candidate_repo_targets"):
        if key not in cache:
            header_failures.append(f"missing top-level key: {key}")
    if str(cache.get("pillar")) != pillar:
        header_failures.append(f"cache pillar mismatch: {cache.get('pillar')}")
    try:
        cache_generated = parse_datetime(str(cache.get("generated_utc")))
    except Exception as exc:  # noqa: BLE001
        header_failures.append(f"invalid generated_utc: {exc}")
        cache_generated = now_utc()
    try:
        refresh_window_days = int(cache.get("refresh_window_days"))
        if refresh_window_days <= 0:
            raise ValueError("must be > 0")
    except Exception as exc:  # noqa: BLE001
        header_failures.append(f"invalid refresh_window_days: {exc}")
        refresh_window_days = 0
    if not header_failures and refresh_window_days > 0:
        age_days = max((now_utc() - cache_generated).days, 0)
        if age_days > refresh_window_days:
            header_warnings.append(f"cache age {age_days}d exceeds refresh window {refresh_window_days}d")
    append_check(checks, "cache_header", header_failures, header_warnings)

    source_failures: list[str] = []
    apis_checked: list[str] = []
    for index, run in enumerate(cache.get("source_runs", []), start=1):
        api_id = str(run.get("api_id", ""))
        if not api_id:
            source_failures.append(f"source_run[{index}] missing api_id")
        else:
            apis_checked.append(api_id)
        if not str(run.get("request_url", "")):
            source_failures.append(f"source_run[{index}] missing request_url")
        if normalize_status(run.get("status")) != "PASS":
            source_failures.append(f"source_run[{index}] non-pass status: {run.get('status')}")
    append_check(checks, "source_runs", source_failures, [])

    record_failures: list[str] = []
    repo_targets_touched: set[str] = set()
    records = cache.get("records", [])
    if not isinstance(records, list) or not records:
        record_failures.append("records must be a non-empty list")
    else:
        for index, record in enumerate(records, start=1):
            missing = sorted(REQUIRED_RECORD_FIELDS - set(record))
            if missing:
                record_failures.append(f"record[{index}] missing fields: {', '.join(missing)}")
                continue
            repo_relevance = record.get("repo_relevance")
            if not isinstance(repo_relevance, dict):
                record_failures.append(f"record[{index}] repo_relevance must be an object")
                continue
            targets = repo_relevance.get("targets")
            if not isinstance(targets, list) or not targets:
                record_failures.append(f"record[{index}] repo_relevance.targets must be a non-empty list")
            else:
                repo_targets_touched.update(str(target) for target in targets)
    append_check(checks, "record_schema", record_failures, [])

    overall_status = "PASS"
    for check in checks:
        overall_status = max(overall_status, normalize_status(check["status"]), key=severity)

    freshness_status = normalize_status(checks[0]["status"])
    next_refresh_action = (
        f"Refresh the cached {pillar} API signals and rerun this board."
        if freshness_status != "PASS"
        else (
            f"Repair the cached {pillar} API schema or rerun the live refresh."
            if overall_status == "FAIL"
            else f"Review promotion candidates before updating curated comparison docs for {pillar}."
        )
    )
    payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "freshness_status": freshness_status,
        "pillar": pillar,
        "cache_path": cache_path,
        "source_count": len(records) if isinstance(records, list) else 0,
        "apis_checked": sorted(set(apis_checked)),
        "repo_targets_touched": sorted(repo_targets_touched),
        "next_refresh_action": next_refresh_action,
        "checks": checks,
        "promotion_candidates": cache.get("candidate_repo_targets", []),
        "effective_success": overall_status == "PASS",
    }
    markdown = render_board_markdown(board_title, payload)
    save_json_and_markdown_run(
        payload=payload,
        markdown=markdown,
        latest_json=latest_json,
        latest_md=latest_md,
        reports_dir=reports_dir,
        stem=f"{pillar}-signal-board",
    )

    print(f"overall_status={overall_status}")
    print(f"source_count={payload['source_count']}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    if fail_on_warn and overall_status != "PASS":
        return 1
    return 0


def render_board_markdown(title: str, payload: dict[str, Any]) -> str:
    lines = [
        f"# {title}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- freshness_status: `{payload['freshness_status']}`",
        f"- source_count: `{payload['source_count']}`",
        f"- apis_checked: `{', '.join(payload['apis_checked']) if payload['apis_checked'] else '-'}`",
        f"- repo_targets_touched: `{', '.join(payload['repo_targets_touched']) if payload['repo_targets_touched'] else '-'}`",
        f"- next_refresh_action: {payload['next_refresh_action']}",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in payload.get("checks", []):
        lines.append(f"| {check['name']} | {check['status']} | {check['detail']} |")

    lines.extend(
        [
            "",
            "## Promotion candidates",
            "| target | record_count | latest_published_at | supporting_source_ids |",
            "|---|---|---|---|",
        ]
    )
    for row in payload.get("promotion_candidates", []):
        lines.append(
            f"| {row.get('target', '-')} | {row.get('record_count', 0)} | {row.get('latest_published_at', '-')} | "
            f"{', '.join(row.get('supporting_source_ids', [])) or '-'} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def api_manifest_status_line(payload: dict[str, Any]) -> str:
    return (
        f"manifest_status={payload.get('overall_status', 'FAIL')}, "
        f"api_count={len(payload.get('apis', [])) if isinstance(payload.get('apis'), list) else 0}"
    )


def quote_plus(raw: str) -> str:
    return urllib.parse.quote_plus(raw)
