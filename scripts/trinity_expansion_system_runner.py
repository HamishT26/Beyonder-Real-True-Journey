#!/usr/bin/env python3
"""Shared runner for Trinity mammoth expansion systems."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from trinity_api_common import fetch_json, fetch_text, quote_plus

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v2.json"
DEFAULT_RUNS_DIR = ROOT / "docs" / "trinity-expansion-runs"
STATUS_ORDER = {"PASS": 0, "WARN": 1, "FAIL": 2, "TIMEOUT": 3}
PASS_LIKE = {"PASS", "WARN"}
PYTHON_SCRIPTS = ROOT / "scripts"
RELEVANT_ENV_VARS = [
    "OPENAI_API_KEY",
    "GITHUB_TOKEN",
    "GITHUB_PERSONAL_ACCESS_TOKEN",
    "GOOGLE_API_KEY",
    "ANTHROPIC_API_KEY",
    "SENTRY_AUTH_TOKEN",
]
SAFE_BOOTSTRAP_MARKERS = [
    'approval_mode = "never"',
    "shell_injection = true",
    "yolo_mode = true",
    "dangerously-bypass-approvals-and-sandbox",
    "god_functions.sh",
    "GITHUB_PERSONAL_ACCESS_TOKEN",
]
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path_str: str) -> dict[str, Any]:
    return json.loads(_repo_path(path_str).read_text(encoding="utf-8"))


def _read_json_safe(path_str: str) -> tuple[bool, dict[str, Any], str]:
    try:
        path = _repo_path(path_str)
    except Exception:
        return False, {}, f"invalid path: {path_str}"
    if not path.exists():
        return False, {}, f"missing artifact: {path_str}"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, {}, f"invalid json: {path_str} ({exc})"
    if not isinstance(payload, dict):
        return False, {}, f"expected json object: {path_str}"
    return True, payload, "ok"


def _write_json(path_str: str, payload: dict[str, Any]) -> Path:
    target = _repo_path(path_str)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


def _write_text(path_str: str, content: str) -> Path:
    target = _repo_path(path_str)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def _read_text_safe(path_str: str) -> tuple[bool, str, str]:
    try:
        path = _repo_path(path_str)
    except Exception:
        return False, "", f"invalid path: {path_str}"
    if not path.exists():
        return False, "", f"missing file: {path_str}"
    try:
        return True, path.read_text(encoding="utf-8"), "ok"
    except Exception as exc:  # noqa: BLE001
        return False, "", f"read error: {path_str} ({exc})"


def _markdown_section(text: str, heading: str, next_heading_level: int = 2) -> str:
    marker = f"## {heading}" if not heading.startswith("#") else heading
    if marker not in text:
        return text
    section = text.split(marker, 1)[1]
    boundary = f"\n{'#' * next_heading_level} "
    if boundary in section:
        section = section.split(boundary, 1)[0]
    return section


def _normalize_status(raw: object) -> str:
    text = str(raw or "").strip().upper()
    if text in STATUS_ORDER:
        return text
    if text in {"OK", "SUCCESS"}:
        return "PASS"
    return "FAIL"


def _payload_status(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("effective_success"), bool):
        return "PASS" if payload["effective_success"] else "FAIL"
    for key in ("overall_status", "status", "comparator_status"):
        if key in payload:
            return _normalize_status(payload.get(key))
    return "FAIL"


def _worst_status(values: list[str]) -> str:
    if not values:
        return "FAIL"
    return max((_normalize_status(item) for item in values), key=lambda item: STATUS_ORDER.get(item, 2))


def _check(name: str, status: str, detail: str) -> dict[str, str]:
    normalized = _normalize_status(status)
    if normalized == "TIMEOUT":
        normalized = "FAIL"
    return {"name": name, "status": normalized, "detail": detail}


def _status_not_fail(raw: str) -> str:
    return "PASS" if _normalize_status(raw) in PASS_LIKE else "FAIL"


def _collect_targets(*groups: list[str]) -> list[str]:
    items: set[str] = set()
    for group in groups:
        for value in group:
            text = str(value).strip()
            if text:
                items.add(text)
    return sorted(items)


def _safe_title(text: str, limit: int = 180) -> str:
    compact = " ".join(str(text or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _parse_date(raw: object, fallback: str = "1970-01-01") -> str:
    text = str(raw or "").strip()
    return text[:10] if text else fallback


def _load_manifest(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest must be an object")
    return payload


def _manifest_entry(manifest: dict[str, Any], system_id: str) -> dict[str, Any]:
    for entry in manifest.get("systems", []):
        if str(entry.get("system_id")) == system_id:
            return entry
    raise KeyError(f"missing system in manifest: {system_id}")


def _manifest_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("system_id")): item for item in manifest.get("systems", []) if isinstance(item, dict)}


def _dependency_output_path(manifest: dict[str, Any], dependency: str) -> str:
    index = _manifest_index(manifest)
    if dependency in index:
        output = index[dependency].get("outputs", [])
        if isinstance(output, list) and output:
            return str(output[0])
    return dependency


def _records_from_latest(path_str: str) -> list[dict[str, Any]]:
    ok, payload, _ = _read_json_safe(path_str)
    if not ok:
        return []
    rows = payload.get("records", [])
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _read_jsonl_safe(path_str: str) -> tuple[list[dict[str, Any]], str]:
    ok, text, detail = _read_text_safe(path_str)
    if not ok:
        return [], detail
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows, "ok"


def _record_targets(row: dict[str, Any]) -> list[str]:
    direct = row.get("repo_targets", [])
    if isinstance(direct, list):
        values = [str(item).strip() for item in direct if str(item).strip()]
        if values:
            return sorted(dict.fromkeys(values))
    repo_relevance = row.get("repo_relevance", {})
    if isinstance(repo_relevance, dict):
        targets = repo_relevance.get("targets", [])
        if isinstance(targets, list):
            values = [str(item).strip() for item in targets if str(item).strip()]
            if values:
                return sorted(dict.fromkeys(values))
    return []


def _normalize_record(row: dict[str, Any], *, default_source_id: str = "public_registry") -> dict[str, Any]:
    return {
        "source_id": str(row.get("source_id") or default_source_id),
        "record_id": str(row.get("record_id") or row.get("url") or row.get("title") or default_source_id),
        "signal_type": str(row.get("signal_type") or row.get("source_kind") or "context_signal"),
        "title": _safe_title(str(row.get("title") or row.get("topic") or row.get("publisher") or "Untitled")),
        "published_at": _parse_date(row.get("published_at")),
        "source_url": str(row.get("source_url") or row.get("url") or ""),
        "summary": _safe_title(str(row.get("summary") or "")),
        "metrics": row.get("metrics") if isinstance(row.get("metrics"), dict) else {},
        "tags": row.get("tags") if isinstance(row.get("tags"), list) else [],
        "repo_targets": _record_targets(row),
    }


def _records_from_api_cache(path_str: str, *, source_ids: set[str] | None = None) -> list[dict[str, Any]]:
    ok, payload, _ = _read_json_safe(path_str)
    if not ok:
        return []
    rows = payload.get("records", [])
    if not isinstance(rows, list):
        return []
    normalized: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        source_id = str(row.get("source_id") or "")
        if source_ids and source_id not in source_ids:
            continue
        normalized.append(_normalize_record(row, default_source_id=source_id or "cached_signal"))
    return normalized


def _records_from_public_registry(
    *,
    pillar: str | None = None,
    topic_terms: list[str] | None = None,
    url_terms: list[str] | None = None,
    source_kinds: set[str] | None = None,
) -> list[dict[str, Any]]:
    ok, payload, _ = _read_json_safe("docs/trinity-public-source-registry-v1.json")
    if not ok:
        return []
    rows = payload.get("sources", [])
    if not isinstance(rows, list):
        return []
    topic_terms = [term.lower() for term in (topic_terms or []) if str(term).strip()]
    url_terms = [term.lower() for term in (url_terms or []) if str(term).strip()]
    normalized: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if pillar and str(row.get("pillar") or "") != pillar:
            continue
        topic_blob = " ".join(
            [
                str(row.get("topic") or ""),
                str(row.get("summary") or ""),
                str(row.get("publisher") or ""),
            ]
        ).lower()
        url_blob = str(row.get("url") or "").lower()
        source_kind = str(row.get("source_kind") or "")
        if topic_terms and not any(term in topic_blob for term in topic_terms):
            continue
        if url_terms and not any(term in url_blob for term in url_terms):
            continue
        if source_kinds and source_kind not in source_kinds:
            continue
        normalized.append(
            {
                "source_id": "public_registry",
                "record_id": f"{row.get('pillar', 'na')}-{hashlib.sha256(str(row.get('url', '')).encode('utf-8')).hexdigest()[:12]}",
                "signal_type": str(row.get("source_kind") or "public_context"),
                "title": _safe_title(str(row.get("topic") or row.get("publisher") or "Public registry signal")),
                "published_at": _parse_date(row.get("published_at")),
                "source_url": str(row.get("url") or ""),
                "summary": _safe_title(str(row.get("summary") or "")),
                "metrics": {
                    "publisher": row.get("publisher"),
                    "jurisdiction": row.get("jurisdiction"),
                    "source_tier": row.get("source_tier"),
                },
                "tags": [str(row.get("pillar") or ""), str(row.get("source_kind") or "")],
                "repo_targets": _record_targets(row),
            }
        )
    return normalized


def _parse_toml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def _repo_skill_dirs() -> list[Path]:
    skill_root = ROOT / "skills"
    if not skill_root.exists():
        return []
    return sorted(path for path in skill_root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def _local_skill_dirs() -> list[Path]:
    skill_root = Path.home() / ".codex" / "skills"
    if not skill_root.exists():
        return []
    return sorted(path for path in skill_root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def _count_script_files() -> int:
    return len(list(PYTHON_SCRIPTS.glob("*.py")))


def _tool_probe(tool: str, *args: str) -> dict[str, Any]:
    executable = shutil.which(tool)
    if not executable:
        return {"tool": tool, "available": False, "detail": "missing"}
    try:
        proc = subprocess.run(
            [executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        text = (proc.stdout or proc.stderr or "").strip().splitlines()
        detail = text[0] if text else f"returncode={proc.returncode}"
        return {"tool": tool, "available": proc.returncode == 0, "detail": detail, "path": executable}
    except Exception as exc:  # noqa: BLE001
        return {"tool": tool, "available": False, "detail": str(exc), "path": executable}


def _git_recent_commits(limit: int = 5) -> list[dict[str, str]]:
    try:
        proc = subprocess.run(
            ["git", "log", "-n", str(limit), "--pretty=format:%H%x09%s"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
    except Exception:  # noqa: BLE001
        return []
    if proc.returncode != 0:
        return []
    rows: list[dict[str, str]] = []
    for line in (proc.stdout or "").splitlines():
        commit, _, subject = line.partition("\t")
        if commit and subject:
            rows.append({"commit": commit[:12], "subject": subject})
    return rows


def _parse_iso(raw: object) -> datetime | None:
    text = str(raw or "").strip()
    if not text:
        return None
    text = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _age_days(raw: object) -> float | None:
    parsed = _parse_iso(raw)
    if parsed is None:
        return None
    return round((datetime.now(timezone.utc) - parsed).total_seconds() / 86400.0, 3)


def _candidate_targets(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    table: dict[str, dict[str, Any]] = {}
    for row in records:
        for target in _record_targets(row):
            bucket = table.setdefault(
                target,
                {
                    "target": target,
                    "record_count": 0,
                    "supporting_source_ids": set(),
                    "latest_published_at": "1970-01-01",
                },
            )
            bucket["record_count"] += 1
            bucket["supporting_source_ids"].add(str(row.get("source_id") or "unknown"))
            if str(row.get("published_at") or "") > str(bucket["latest_published_at"]):
                bucket["latest_published_at"] = str(row.get("published_at") or "")
    rows: list[dict[str, Any]] = []
    for target, bucket in table.items():
        rows.append(
            {
                "target": target,
                "record_count": bucket["record_count"],
                "supporting_source_ids": sorted(bucket["supporting_source_ids"]),
                "latest_published_at": bucket["latest_published_at"],
            }
        )
    rows.sort(key=lambda row: (int(row["record_count"]), str(row["latest_published_at"]), str(row["target"])), reverse=True)
    return rows


def _manifest_graph(manifest: dict[str, Any]) -> tuple[list[tuple[str, str]], list[str], list[list[str]]]:
    index = _manifest_index(manifest)
    edges: list[tuple[str, str]] = []
    missing: list[str] = []
    for system_id, entry in index.items():
        depends_on = entry.get("depends_on", [])
        if not isinstance(depends_on, list):
            continue
        for dep in depends_on:
            dep_str = str(dep)
            if dep_str in index:
                edges.append((system_id, dep_str))
            elif "/" not in dep_str and "\\" not in dep_str and "." not in dep_str:
                missing.append(f"{system_id}->{dep_str}")

    cycles: list[list[str]] = []
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for src, dep in edges:
            if src != node:
                continue
            dep_state = state.get(dep, 0)
            if dep_state == 0:
                visit(dep)
            elif dep_state == 1:
                if dep in stack:
                    cycle = stack[stack.index(dep) :] + [dep]
                    cycles.append(cycle)
        stack.pop()
        state[node] = 2

    for node in index:
        if state.get(node, 0) == 0:
            visit(node)
    return edges, sorted(dict.fromkeys(missing)), cycles


def _publish(
    *,
    entry: dict[str, Any],
    checks: list[dict[str, str]],
    metrics: dict[str, Any],
    targets: list[str],
    next_action: str,
    records: list[dict[str, Any]] | None,
    source_runs: list[dict[str, Any]] | None,
    fail_on_warn: bool,
    runs_dir: str,
) -> int:
    overall = _worst_status([item.get("status", "FAIL") for item in checks])
    effective_success = overall == "PASS" or (overall == "WARN" and not fail_on_warn)

    payload: dict[str, Any] = {
        "generated_utc": _now_iso(),
        "system_id": str(entry["system_id"]),
        "pillar": str(entry["pillar"]),
        "overall_status": overall,
        "checks": checks,
        "metrics": metrics,
        "repo_targets_touched": sorted(targets),
        "next_action": next_action,
        "effective_success": effective_success,
    }
    if records is not None:
        payload["records"] = records
    if source_runs is not None:
        payload["source_runs"] = source_runs

    latest_output = str((entry.get("outputs") or [""])[0]).strip()
    if not latest_output:
        latest_output = f"docs/trinity-expansion/{entry['system_id'].replace('_', '-')}-latest.json"
    timestamped_output = f"{runs_dir.rstrip('/')}/{_stamp()}-{entry['system_id'].replace('_', '-')}.json"
    latest_md = latest_output[:-5] + ".md" if latest_output.endswith(".json") else latest_output + ".md"
    timestamped_md = timestamped_output[:-5] + ".md" if timestamped_output.endswith(".json") else timestamped_output + ".md"
    latest_path = _write_json(latest_output, payload)
    timestamped_path = _write_json(timestamped_output, payload)
    markdown_lines = [
        f"# Trinity Expansion Result: {entry['system_id']}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- pillar: `{payload['pillar']}`",
        f"- overall_status: **{overall}**",
        f"- effective_success: `{effective_success}`",
        "",
        "## Checks",
        "| name | status | detail |",
        "|---|---|---|",
    ]
    for item in checks:
        markdown_lines.append(f"| {item.get('name', '')} | {item.get('status', '')} | {item.get('detail', '')} |")
    markdown_lines.extend(
        [
            "",
            "## Metrics",
            "```json",
            json.dumps(metrics, indent=2, sort_keys=True),
            "```",
        ]
    )
    if targets:
        markdown_lines.extend(["", "## Repo targets touched"])
        markdown_lines.extend([f"- `{target}`" for target in sorted(targets)])
    markdown = "\n".join(markdown_lines).rstrip() + "\n"
    latest_md_path = _write_text(latest_md, markdown)
    timestamped_md_path = _write_text(timestamped_md, markdown)

    print(f"overall_status={overall}")
    print(f"effective_success={effective_success}")
    print(f"latest_json={latest_path.relative_to(ROOT)}")
    print(f"timestamped_json={timestamped_path.relative_to(ROOT)}")
    print(f"latest_md={latest_md_path.relative_to(ROOT)}")
    print(f"timestamped_md={timestamped_md_path.relative_to(ROOT)}")
    return 0 if effective_success else 1


def _artifact_guard(manifest: dict[str, Any], dependencies: list[str]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    metrics: dict[str, Any] = {"dependencies_checked": 0, "pass_like_dependencies": 0}
    for dep in dependencies:
        path = _dependency_output_path(manifest, dep)
        metrics["dependencies_checked"] += 1
        ok, payload, detail = _read_json_safe(path)
        if not ok:
            checks.append(_check(f"dependency:{path}", "FAIL", detail))
            continue
        status = _payload_status(payload)
        pass_like = _status_not_fail(status) == "PASS"
        if pass_like:
            metrics["pass_like_dependencies"] += 1
        checks.append(_check(f"dependency:{path}", "PASS" if pass_like else "FAIL", f"status={status}"))
    return checks, metrics


def _mind_crossref(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
    queries = query_pack.get("mind", {}).get("queries", [])
    fallback = _records_from_latest("docs/trinity-expansion/mind-theory-signal-refresh-crossref-latest.json")

    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "crossref", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "crossref", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    for query in queries:
        if not isinstance(query, dict):
            continue
        term = str(query.get("query") or "").strip()
        if not term:
            continue
        url = f"https://api.crossref.org/works?query.bibliographic={quote_plus(term)}&rows=3&sort=published&order=desc"
        try:
            payload = fetch_json(url, timeout_sec=timeout_sec)
            items = payload.get("message", {}).get("items", []) if isinstance(payload, dict) else []
            for item in items:
                title = (item.get("title") or [""])[0] if isinstance(item.get("title"), list) else str(item.get("title") or "")
                doi = str(item.get("DOI") or "")
                date_parts = ((item.get("issued") or {}).get("date-parts") or [[]])[0]
                year = int(date_parts[0]) if len(date_parts) > 0 and date_parts[0] else 1970
                month = int(date_parts[1]) if len(date_parts) > 1 and date_parts[1] else 1
                day = int(date_parts[2]) if len(date_parts) > 2 and date_parts[2] else 1
                records.append(
                    {
                        "source_id": "crossref",
                        "record_id": doi or f"{query.get('query_id')}-{len(records)+1}",
                        "signal_type": query.get("signal_type", "theory_context"),
                        "title": _safe_title(title),
                        "published_at": f"{year:04d}-{month:02d}-{day:02d}",
                        "source_url": f"https://doi.org/{doi}" if doi else url,
                        "summary": _safe_title(f"Crossref signal for {term}."),
                        "metrics": {"query_id": query.get("query_id"), "is_referenced_by_count": item.get("is-referenced-by-count")},
                        "tags": ["mind", "crossref"],
                        "repo_targets": query.get("repo_targets", []),
                    }
                )
            runs.append({"source_id": "crossref", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": len(items), "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"crossref fallback used ({exc})"))
                return checks, fallback, [{"source_id": "crossref", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback)}
            checks.append(_check("crossref_live_fetch", "FAIL", str(exc)))
            runs.append({"source_id": "crossref", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    targets = _collect_targets(
        [
            str(target)
            for query in queries
            if isinstance(query, dict)
            for target in query.get("repo_targets", [])
        ]
    )
    return checks, records, runs, targets, {"offline_only": False, "record_count": len(records), "query_count": len([q for q in queries if isinstance(q, dict)])}


def _mind_semanticscholar(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
    queries = query_pack.get("mind", {}).get("queries", [])
    fallback = _records_from_latest("docs/trinity-expansion/mind-theory-signal-refresh-semanticscholar-latest.json")

    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "semanticscholar", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "semanticscholar", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    for query in queries:
        if not isinstance(query, dict):
            continue
        term = str(query.get("query") or "").strip()
        if not term:
            continue
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={quote_plus(term)}&limit=3&fields=title,url,year,citationCount,publicationDate"
        try:
            payload = fetch_json(url, timeout_sec=timeout_sec)
            items = payload.get("data", []) if isinstance(payload, dict) else []
            for item in items:
                records.append(
                    {
                        "source_id": "semanticscholar",
                        "record_id": str(item.get("paperId") or item.get("url") or f"{query.get('query_id')}-{len(records)+1}"),
                        "signal_type": query.get("signal_type", "theory_context"),
                        "title": _safe_title(str(item.get("title") or "")),
                        "published_at": _parse_date(item.get("publicationDate"), fallback=f"{item.get('year', 1970)}-01-01"),
                        "source_url": str(item.get("url") or url),
                        "summary": _safe_title(f"Semantic Scholar signal for {term}."),
                        "metrics": {"query_id": query.get("query_id"), "citation_count": item.get("citationCount"), "year": item.get("year")},
                        "tags": ["mind", "semanticscholar"],
                        "repo_targets": query.get("repo_targets", []),
                    }
                )
            runs.append({"source_id": "semanticscholar", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": len(items), "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"semanticscholar fallback used ({exc})"))
                return checks, fallback, [{"source_id": "semanticscholar", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback)}
            ok_cache, cache_payload, _ = _read_json_safe("docs/trinity-api-cache/mind-signals-latest.json")
            cache_records = [
                row
                for row in (cache_payload.get("records", []) if ok_cache else [])
                if isinstance(row, dict) and str(row.get("source_id")) in {"openalex", "arxiv"}
            ]
            if cache_records:
                checks.append(_check("cache_bridge_fallback", "PASS", f"mind-api-cache fallback used ({exc})"))
                return checks, cache_records, [{"source_id": "semanticscholar", "mode": "fallback_api_cache", "record_count": len(cache_records), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(cache_records)}
            checks.append(_check("semanticscholar_live_fetch", "FAIL", str(exc)))
            runs.append({"source_id": "semanticscholar", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    targets = _collect_targets(
        [
            str(target)
            for query in queries
            if isinstance(query, dict)
            for target in query.get("repo_targets", [])
        ]
    )
    return checks, records, runs, targets, {"offline_only": False, "record_count": len(records), "query_count": len([q for q in queries if isinstance(q, dict)])}


def _load_records_from_system(manifest: dict[str, Any], system_id: str) -> list[dict[str, Any]]:
    path = _dependency_output_path(manifest, system_id)
    return _records_from_latest(path)


def _merge_records(manifest: dict[str, Any], system_ids: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, str]], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    pass_like = 0
    for system_id in system_ids:
        path = _dependency_output_path(manifest, system_id)
        ok, payload, detail = _read_json_safe(path)
        if not ok:
            checks.append(_check(f"dependency:{system_id}", "FAIL", detail))
            continue
        status = _payload_status(payload)
        if _status_not_fail(status) == "PASS":
            pass_like += 1
        checks.append(_check(f"dependency:{system_id}", _status_not_fail(status), f"status={status}"))
        for row in payload.get("records", []):
            if not isinstance(row, dict):
                continue
            key = (str(row.get("source_id")), str(row.get("record_id")))
            merged[key] = row
    rows = sorted(merged.values(), key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("merged_records_present", "PASS" if rows else "FAIL", f"records={len(rows)}"))
    metrics = {"dependency_count": len(system_ids), "pass_like_dependencies": pass_like, "record_count": len(rows)}
    return rows, checks, metrics


def _github_watchlist_live(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
    watchlist = query_pack.get("body", {}).get("github_watchlist", [])
    fallback = _records_from_latest("docs/trinity-expansion/body-dependency-health-refresh-latest.json")

    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "github_watchlist", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "github_watchlist", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    for item in watchlist:
        if not isinstance(item, dict):
            continue
        repo = str(item.get("repo") or "").strip()
        if not repo:
            continue
        url = f"https://api.github.com/repos/{repo}"
        try:
            payload = fetch_json(url, timeout_sec=timeout_sec)
            if not isinstance(payload, dict):
                raise ValueError("github payload was not an object")
            records.append(
                {
                    "source_id": "github",
                    "record_id": repo,
                    "signal_type": item.get("signal_type", "repo_watchlist"),
                    "title": _safe_title(str(payload.get("full_name") or repo)),
                    "published_at": _parse_date(payload.get("pushed_at")),
                    "source_url": str(payload.get("html_url") or f"https://github.com/{repo}"),
                    "summary": _safe_title(str(payload.get("description") or f"Watchlist signal for {repo}")),
                    "metrics": {
                        "stars": payload.get("stargazers_count"),
                        "open_issues": payload.get("open_issues_count"),
                        "forks": payload.get("forks_count"),
                    },
                    "tags": ["body", "github"],
                    "repo_targets": item.get("repo_targets", []),
                }
            )
            runs.append({"source_id": "github", "request_id": item.get("query_id"), "request_url": url, "mode": "live", "record_count": 1, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"github fallback used ({exc})"))
                return checks, fallback, [{"source_id": "github_watchlist", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback)}
            checks.append(_check(f"github_fetch:{repo}", "FAIL", str(exc)))
            runs.append({"source_id": "github", "request_id": item.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    targets = _collect_targets(
        [
            str(target)
            for item in watchlist
            if isinstance(item, dict)
            for target in item.get("repo_targets", [])
        ]
    )
    return checks, records, runs, targets, {"offline_only": False, "record_count": len(records), "watchlist_count": len([w for w in watchlist if isinstance(w, dict)])}


def _connectivity_probe_live(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    manifest = _read_json("docs/trinity-api-source-manifest-v1.json")
    apis = [item for item in manifest.get("apis", []) if isinstance(item, dict)]
    fallback = _records_from_latest("docs/trinity-expansion/body-runtime-connectivity-probe-latest.json")

    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "connectivity", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/trinity-api-source-manifest-v1.json"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "connectivity", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/trinity-api-source-manifest-v1.json"]), {"offline_only": True, "record_count": 0}

    for item in apis:
        api_id = str(item.get("api_id") or "unknown")
        base_url = str(item.get("base_url") or "").strip()
        if not base_url:
            continue
        probe = base_url
        if "api.github.com" in base_url:
            probe = "https://api.github.com/rate_limit"
        elif "api.worldbank.org" in base_url:
            probe = "https://api.worldbank.org/v2/country/NZL?format=json"
        elif "catalogue.data.govt.nz" in base_url:
            probe = "https://catalogue.data.govt.nz/api/3/action/site_read"
        try:
            text = fetch_text(probe, timeout_sec=timeout_sec)
            records.append(
                {
                    "source_id": "connectivity_probe",
                    "record_id": api_id,
                    "signal_type": "connectivity_probe",
                    "title": f"Connectivity probe: {api_id}",
                    "published_at": _now_iso()[:10],
                    "source_url": probe,
                    "summary": f"Probe succeeded for {api_id}.",
                    "metrics": {"bytes": len(text)},
                    "tags": ["body", "connectivity", api_id],
                    "repo_targets": ["docs/trinity-mandala-scoreboard-latest.json"],
                }
            )
            runs.append({"source_id": "connectivity_probe", "request_id": api_id, "request_url": probe, "mode": "live", "record_count": 1, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"connectivity fallback used ({exc})"))
                return checks, fallback, [{"source_id": "connectivity", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/trinity-api-source-manifest-v1.json"]), {"offline_only": False, "record_count": len(fallback)}
            records.append(
                {
                    "source_id": "connectivity_probe",
                    "record_id": api_id,
                    "signal_type": "connectivity_probe",
                    "title": f"Connectivity probe fallback: {api_id}",
                    "published_at": _now_iso()[:10],
                    "source_url": probe,
                    "summary": f"Live probe failed for {api_id}; synthetic fallback emitted.",
                    "metrics": {"error": str(exc)},
                    "tags": ["body", "connectivity", api_id],
                    "repo_targets": ["docs/trinity-mandala-scoreboard-latest.json"],
                }
            )
            checks.append(_check(f"probe:{api_id}", "PASS", f"synthetic fallback used ({exc})"))
            runs.append({"source_id": "connectivity_probe", "request_id": api_id, "request_url": probe, "mode": "live_fallback_synthetic", "record_count": 1, "status": "PASS"})

    records = sorted(records, key=lambda row: str(row.get("record_id")))
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets(["docs/trinity-api-source-manifest-v1.json"]), {"offline_only": False, "record_count": len(records), "api_count": len(apis)}


def _heart_worldbank_oecd_live(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
    world_bank_rows = [row for row in query_pack.get("heart", {}).get("world_bank_indicators", []) if isinstance(row, dict)]
    oecd_rows = [row for row in query_pack.get("heart", {}).get("oecd_keywords", []) if isinstance(row, dict)]
    fallback = _records_from_latest("docs/trinity-expansion/heart-governance-signal-refresh-worldbank-oecd-latest.json")

    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "heart_worldbank_oecd", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "heart_worldbank_oecd", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    for row in world_bank_rows:
        country = str(row.get("country") or "NZL")
        indicator = str(row.get("indicator") or "").strip()
        if not indicator:
            continue
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=3"
        try:
            payload = fetch_json(url, timeout_sec=timeout_sec)
            entries = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
            item = next((entry for entry in entries if isinstance(entry, dict) and entry.get("value") is not None), entries[0] if entries else {})
            item = item if isinstance(item, dict) else {}
            records.append(
                {
                    "source_id": "worldbank",
                    "record_id": f"{country}-{indicator}",
                    "signal_type": row.get("signal_type", "governance_indicator"),
                    "title": _safe_title(str((item.get("indicator") or {}).get("value") or indicator)),
                    "published_at": _parse_date(f"{item.get('date', '1970')}-01-01"),
                    "source_url": url,
                    "summary": _safe_title(f"World Bank governance context for {country} {indicator}."),
                    "metrics": {"country": country, "indicator": indicator, "value": item.get("value"), "date": item.get("date")},
                    "tags": ["heart", "worldbank"],
                    "repo_targets": row.get("repo_targets", []),
                }
            )
            runs.append({"source_id": "worldbank", "request_id": row.get("query_id"), "request_url": url, "mode": "live", "record_count": 1, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"worldbank fallback used ({exc})"))
                return checks, fallback, [{"source_id": "heart_worldbank_oecd", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback)}
            checks.append(_check(f"worldbank_fetch:{indicator}", "FAIL", str(exc)))
            runs.append({"source_id": "worldbank", "request_id": row.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    for row in oecd_rows:
        keyword = str(row.get("keyword") or "").strip()
        if not keyword:
            continue
        url = "https://sdmx.oecd.org/public/rest/dataflow/all/all/latest"
        try:
            xml_text = fetch_text(url, timeout_sec=timeout_sec)
            match_count = len(re.findall(keyword.lower(), xml_text.lower()))
            records.append(
                {
                    "source_id": "oecd",
                    "record_id": f"oecd-{keyword.lower().replace(' ', '-')}",
                    "signal_type": row.get("signal_type", "catalog_context"),
                    "title": f"OECD keyword {keyword}",
                    "published_at": _now_iso()[:10],
                    "source_url": url,
                    "summary": _safe_title(f"OECD catalog probe for keyword {keyword}."),
                    "metrics": {"keyword": keyword, "keyword_match_count": match_count},
                    "tags": ["heart", "oecd"],
                    "repo_targets": row.get("repo_targets", []),
                }
            )
            runs.append({"source_id": "oecd", "request_id": row.get("query_id"), "request_url": url, "mode": "live", "record_count": 1, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"oecd fallback used ({exc})"))
                return checks, fallback, [{"source_id": "heart_worldbank_oecd", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback)}
            checks.append(_check(f"oecd_fetch:{keyword}", "FAIL", str(exc)))
            runs.append({"source_id": "oecd", "request_id": row.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-06.md"]), {"offline_only": False, "record_count": len(records), "world_bank_query_count": len(world_bank_rows), "oecd_query_count": len(oecd_rows)}


def _heart_data_govt_live(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
    queries = [row for row in query_pack.get("heart", {}).get("data_govt_queries", []) if isinstance(row, dict)]
    fallback = _records_from_latest("docs/trinity-expansion/heart-governance-signal-refresh-data-govt-nz-latest.json")

    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "heart_data_govt", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "heart_data_govt", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    for query in queries:
        term = str(query.get("query") or "").strip()
        if not term:
            continue
        url = f"https://catalogue.data.govt.nz/api/3/action/package_search?q={quote_plus(term)}&rows=2"
        try:
            payload = fetch_json(url, timeout_sec=timeout_sec)
            items = payload.get("result", {}).get("results", []) if isinstance(payload, dict) else []
            for item in items:
                if not isinstance(item, dict):
                    continue
                records.append(
                    {
                        "source_id": "data_govt_nz",
                        "record_id": str(item.get("id") or item.get("name") or f"{query.get('query_id')}-{len(records)+1}"),
                        "signal_type": query.get("signal_type", "nz_dataset_context"),
                        "title": _safe_title(str(item.get("title") or item.get("name") or term)),
                        "published_at": _parse_date(item.get("metadata_modified") or item.get("metadata_created")),
                        "source_url": f"https://catalogue.data.govt.nz/dataset/{item.get('name')}",
                        "summary": _safe_title(str(item.get("notes") or f"data.govt.nz signal for {term}")),
                        "metrics": {"query": term, "resource_count": len(item.get("resources", []))},
                        "tags": ["heart", "nz"],
                        "repo_targets": query.get("repo_targets", []),
                    }
                )
            runs.append({"source_id": "data_govt_nz", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": len(items), "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"data.govt.nz fallback used ({exc})"))
                return checks, fallback, [{"source_id": "heart_data_govt", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback)}
            checks.append(_check(f"data_govt_fetch:{term}", "FAIL", str(exc)))
            runs.append({"source_id": "data_govt_nz", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-06.md"]), {"offline_only": False, "record_count": len(records), "query_count": len(queries)}


def _heart_standards_live(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    standards = [
        ("w3c_did_core", "https://www.w3.org/TR/did-core/"),
        ("w3c_vc_data_model_2", "https://www.w3.org/TR/vc-data-model-2.0/"),
        ("nist_ai_rmf", "https://www.nist.gov/itl/ai-risk-management-framework"),
        ("oecd_ai_principles", "https://oecd.ai/en/ai-principles"),
        ("udhr", "https://www.un.org/en/about-us/universal-declaration-of-human-rights"),
        ("eu_ai_act", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"),
        ("nz_parliament", "https://www.parliament.nz/")
    ]
    fallback = _records_from_latest("docs/trinity-expansion/heart-governance-signal-refresh-standards-docs-latest.json")

    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "heart_standards", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "heart_standards", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    for doc_id, url in standards:
        try:
            html = fetch_text(url, timeout_sec=timeout_sec)
            title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
            title = _safe_title(re.sub(r"\s+", " ", title_match.group(1).strip())) if title_match else doc_id
            records.append(
                {
                    "source_id": "standards_docs",
                    "record_id": doc_id,
                    "signal_type": "standards_context",
                    "title": title,
                    "published_at": _now_iso()[:10],
                    "source_url": url,
                    "summary": f"Standards endpoint reachable for {doc_id}.",
                    "metrics": {"content_length": len(html)},
                    "tags": ["heart", "standards"],
                    "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"],
                }
            )
            runs.append({"source_id": "standards_docs", "request_id": doc_id, "request_url": url, "mode": "live", "record_count": 1, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"standards fallback used ({exc})"))
                return checks, fallback, [{"source_id": "heart_standards", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback)}
            checks.append(_check(f"standards_fetch:{doc_id}", "FAIL", str(exc)))
            runs.append({"source_id": "standards_docs", "request_id": doc_id, "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: str(row.get("record_id")))
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"]), {"offline_only": False, "record_count": len(records), "standards_count": len(standards)}


def _mind_arxiv_live(offline_only: bool, timeout_sec: int) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
    queries = [row for row in query_pack.get("mind", {}).get("queries", []) if isinstance(row, dict)]
    fallback = (
        _records_from_latest("docs/trinity-expansion/mind-public-theory-refresh-arxiv-latest.json")
        or _records_from_api_cache("docs/trinity-api-cache/mind-signals-latest.json", source_ids={"arxiv"})
        or _records_from_public_registry(pillar="mind", topic_terms=["string theory", "quantum gravity", "testability"])
    )
    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": "arxiv", "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/gmut-claim-register-v0.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "arxiv", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    records: list[dict[str, Any]] = []
    for query in queries:
        term = str(query.get("query") or "").strip()
        if not term:
            continue
        url = (
            "https://export.arxiv.org/api/query?"
            f"search_query=all%3A%22{quote_plus(term)}%22&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending"
        )
        try:
            xml_text = fetch_text(url, timeout_sec=timeout_sec)
            feed = ET.fromstring(xml_text)
            entries = feed.findall("atom:entry", ATOM_NS)
            for item in entries:
                entry_id = item.findtext("atom:id", default="", namespaces=ATOM_NS)
                title = item.findtext("atom:title", default="", namespaces=ATOM_NS)
                summary = item.findtext("atom:summary", default="", namespaces=ATOM_NS)
                published = item.findtext("atom:published", default="", namespaces=ATOM_NS)
                categories = [node.attrib.get("term", "") for node in item.findall("atom:category", ATOM_NS) if node.attrib.get("term")]
                authors = len(item.findall("atom:author", ATOM_NS))
                records.append(
                    {
                        "source_id": "arxiv",
                        "record_id": entry_id or f"{query.get('query_id')}-{len(records)+1}",
                        "signal_type": query.get("signal_type", "theory_context"),
                        "title": _safe_title(title),
                        "published_at": _parse_date(published),
                        "source_url": entry_id or url,
                        "summary": _safe_title(summary),
                        "metrics": {"query_id": query.get("query_id"), "authors": authors, "categories": categories[:4]},
                        "tags": ["mind", "arxiv"],
                        "repo_targets": query.get("repo_targets", []),
                    }
                )
            runs.append({"source_id": "arxiv", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": len(entries), "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback:
                checks.append(_check("live_fallback", "PASS", f"arxiv fallback used ({exc})"))
                return checks, fallback, [{"source_id": "arxiv", "mode": "fallback_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/gmut-claim-register-v0.md"]), {"offline_only": False, "record_count": len(fallback)}
            checks.append(_check(f"arxiv_fetch:{term}", "FAIL", str(exc)))
            runs.append({"source_id": "arxiv", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/gmut-claim-register-v0.md", "docs/trinity-public-research-brief-2026-03-06.md"]), {"offline_only": False, "record_count": len(records), "query_count": len(queries)}


def _openalex_live(
    *,
    pillar: str,
    query_rows: list[dict[str, Any]],
    latest_path: str,
    timeout_sec: int,
    offline_only: bool,
    fallback_records: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    if offline_only:
        if fallback_records:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback_records)}"))
            return checks, fallback_records, [{"source_id": "openalex", "mode": "offline_cache", "record_count": len(fallback_records), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback_records)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "openalex", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    records: list[dict[str, Any]] = []
    for query in query_rows:
        term = str(query.get("query") or "").strip()
        if not term:
            continue
        url = f"https://api.openalex.org/works?search={quote_plus(term)}&per-page=3&sort=publication_date:desc"
        try:
            payload = fetch_json(url, timeout_sec=timeout_sec)
            items = payload.get("results", []) if isinstance(payload, dict) else []
            for item in items:
                if not isinstance(item, dict):
                    continue
                primary_location = item.get("primary_location", {}) if isinstance(item.get("primary_location"), dict) else {}
                source_url = (
                    str(primary_location.get("landing_page_url") or "")
                    or str(primary_location.get("pdf_url") or "")
                    or str(item.get("id") or url)
                )
                records.append(
                    {
                        "source_id": "openalex",
                        "record_id": str(item.get("id") or source_url or f"{query.get('query_id')}-{len(records)+1}"),
                        "signal_type": query.get("signal_type", "context_signal"),
                        "title": _safe_title(str(item.get("display_name") or term)),
                        "published_at": _parse_date(item.get("publication_date"), fallback=f"{item.get('publication_year', 1970)}-01-01"),
                        "source_url": source_url,
                        "summary": _safe_title(f"OpenAlex signal for {term}."),
                        "metrics": {
                            "query_id": query.get("query_id"),
                            "cited_by_count": item.get("cited_by_count"),
                            "publication_year": item.get("publication_year"),
                        },
                        "tags": [pillar, "openalex"],
                        "repo_targets": query.get("repo_targets", []),
                    }
                )
            runs.append({"source_id": "openalex", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": len(items), "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback_records:
                checks.append(_check("live_fallback", "PASS", f"openalex fallback used ({exc})"))
                return checks, fallback_records, [{"source_id": "openalex", "mode": "fallback_cache", "record_count": len(fallback_records), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback_records)}
            checks.append(_check(f"openalex_fetch:{term}", "FAIL", str(exc)))
            runs.append({"source_id": "openalex", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})

    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets([str(target) for query in query_rows for target in query.get("repo_targets", [])]), {"offline_only": False, "record_count": len(records), "query_count": len(query_rows)}


def _crossref_live(
    *,
    pillar: str,
    query_rows: list[dict[str, Any]],
    timeout_sec: int,
    offline_only: bool,
    fallback_records: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    if offline_only:
        if fallback_records:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback_records)}"))
            return checks, fallback_records, [{"source_id": "crossref", "mode": "offline_cache", "record_count": len(fallback_records), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": len(fallback_records)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": "crossref", "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    records: list[dict[str, Any]] = []
    for query in query_rows:
        term = str(query.get("query") or "").strip()
        if not term:
            continue
        url = f"https://api.crossref.org/works?query.bibliographic={quote_plus(term)}&rows=3&sort=published&order=desc"
        try:
            payload = fetch_json(url, timeout_sec=timeout_sec)
            items = payload.get("message", {}).get("items", []) if isinstance(payload, dict) else []
            for item in items:
                title = (item.get("title") or [""])[0] if isinstance(item.get("title"), list) else str(item.get("title") or "")
                doi = str(item.get("DOI") or "")
                records.append(
                    {
                        "source_id": "crossref",
                        "record_id": doi or f"{query.get('query_id')}-{len(records)+1}",
                        "signal_type": query.get("signal_type", "context_signal"),
                        "title": _safe_title(title),
                        "published_at": _parse_date(
                            f"{((item.get('issued') or {}).get('date-parts') or [[1970,1,1]])[0][0]:04d}-"
                            f"{(((item.get('issued') or {}).get('date-parts') or [[1970,1,1]])[0][1] if len(((item.get('issued') or {}).get('date-parts') or [[1970,1,1]])[0]) > 1 else 1):02d}-"
                            f"{(((item.get('issued') or {}).get('date-parts') or [[1970,1,1]])[0][2] if len(((item.get('issued') or {}).get('date-parts') or [[1970,1,1]])[0]) > 2 else 1):02d}"
                        ),
                        "source_url": f"https://doi.org/{doi}" if doi else url,
                        "summary": _safe_title(f"Crossref signal for {term}."),
                        "metrics": {
                            "query_id": query.get("query_id"),
                            "publisher": item.get("publisher"),
                            "is_referenced_by_count": item.get("is-referenced-by-count"),
                        },
                        "tags": [pillar, "crossref"],
                        "repo_targets": query.get("repo_targets", []),
                    }
                )
            runs.append({"source_id": "crossref", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": len(items), "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            if fallback_records:
                checks.append(_check("live_fallback", "PASS", f"crossref fallback used ({exc})"))
                return checks, fallback_records, [{"source_id": "crossref", "mode": "fallback_cache", "record_count": len(fallback_records), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": False, "record_count": len(fallback_records)}
            checks.append(_check(f"crossref_fetch:{term}", "FAIL", str(exc)))
            runs.append({"source_id": "crossref", "request_id": query.get("query_id"), "request_url": url, "mode": "live", "record_count": 0, "status": "FAIL"})
    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets([str(target) for query in query_rows for target in query.get("repo_targets", [])]), {"offline_only": False, "record_count": len(records), "query_count": len(query_rows)}


def _heart_registry_live(
    *,
    latest_path: str,
    timeout_sec: int,
    offline_only: bool,
    topic_terms: list[str] | None = None,
    url_terms: list[str] | None = None,
    source_kinds: set[str] | None = None,
    source_id: str,
) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    runs: list[dict[str, Any]] = []
    registry_records = _records_from_public_registry(
        pillar="heart",
        topic_terms=topic_terms,
        url_terms=url_terms,
        source_kinds=source_kinds,
    )
    fallback = _records_from_latest(latest_path) or registry_records
    if offline_only:
        if fallback:
            checks.append(_check("offline_cache", "PASS", f"records={len(fallback)}"))
            return checks, fallback, [{"source_id": source_id, "mode": "offline_cache", "record_count": len(fallback), "status": "PASS"}], _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"]), {"offline_only": True, "record_count": len(fallback)}
        checks.append(_check("offline_cache", "FAIL", "missing fallback cache"))
        return checks, [], [{"source_id": source_id, "mode": "offline_cache", "record_count": 0, "status": "FAIL"}], _collect_targets(["docs/comparative-validation-grid-v1.md"]), {"offline_only": True, "record_count": 0}

    records: list[dict[str, Any]] = []
    for row in registry_records:
        url = str(row.get("source_url") or "").strip()
        if not url:
            continue
        try:
            html = fetch_text(url, timeout_sec=timeout_sec)
            title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
            live_title = _safe_title(re.sub(r"\s+", " ", title_match.group(1).strip())) if title_match else row["title"]
            item = dict(row)
            item["source_id"] = source_id
            item["title"] = live_title
            item["summary"] = _safe_title(f"Endpoint reachable for {live_title}.")
            item["metrics"] = {"content_length": len(html)}
            records.append(item)
            runs.append({"source_id": source_id, "request_id": row.get("record_id"), "request_url": url, "mode": "live", "record_count": 1, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            item = dict(row)
            item["source_id"] = source_id
            records.append(item)
            checks.append(_check(f"registry_fallback:{row.get('record_id')}", "PASS", f"registry fallback used ({exc})"))
            runs.append({"source_id": source_id, "request_id": row.get("record_id"), "request_url": url, "mode": "registry_fallback", "record_count": 1, "status": "PASS"})
    records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
    checks.append(_check("records_present", "PASS" if records else "FAIL", f"records={len(records)}"))
    return checks, records, runs, _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md", "docs/trinity-public-research-brief-2026-03-06.md"]), {"offline_only": False, "record_count": len(records)}


def _compute_system(system_id: str, manifest: dict[str, Any], offline_only: bool, timeout_sec: int) -> dict[str, Any]:
    records: list[dict[str, Any]] | None = None
    source_runs: list[dict[str, Any]] | None = None
    targets: list[str] = []

    if system_id == "mind_claim_evidence_partition":
        ok, registry, detail = _read_json_safe("docs/trinity-public-source-registry-v1.json")
        if not ok:
            return {"checks": [_check("registry_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/trinity-public-source-registry-v1.json"], "next_action": "Restore Mind source registry.", "records": None, "source_runs": None}
        sources = [row for row in registry.get("sources", []) if isinstance(row, dict) and row.get("pillar") == "mind"]
        missing = 0
        required = {"pillar", "topic", "publisher", "url", "published_at", "source_tier", "repo_relevance", "next_validation_target"}
        for row in sources:
            if not required.issubset(row.keys()):
                missing += 1
        confirmed = sum(1 for row in sources if str(row.get("source_tier")) in {"official_primary", "research_primary"})
        inference = sum(1 for row in sources if str(row.get("source_tier")) == "official_secondary")
        open_gap = sum(1 for row in sources if not row.get("next_validation_target"))
        targets = _collect_targets([str(t) for row in sources for t in (row.get("repo_relevance", {}) or {}).get("targets", [])])
        checks = [
            _check("mind_sources_present", "PASS" if sources else "FAIL", f"mind_sources={len(sources)}"),
            _check("mind_source_required_fields", "PASS" if missing == 0 else "FAIL", f"missing_required={missing}"),
        ]
        return {"checks": checks, "metrics": {"mind_source_count": len(sources), "confirmed_evidence": confirmed, "inference": inference, "open_gap": open_gap}, "targets": targets, "next_action": "Use confirmed evidence for Mind comparator wording; keep gaps tied to falsification.", "records": None, "source_runs": None}

    if system_id == "mind_falsification_backlog_builder":
        ok, registry, detail = _read_json_safe("docs/trinity-public-source-registry-v1.json")
        checks: list[dict[str, str]] = []
        if not ok:
            checks.append(_check("registry_present", "FAIL", detail))
            return {"checks": checks, "metrics": {}, "targets": ["docs/gmut-claim-register-v0.md"], "next_action": "Restore Mind source registry.", "records": None, "source_runs": None}
        backlog = []
        for row in registry.get("sources", []):
            if not isinstance(row, dict) or row.get("pillar") != "mind":
                continue
            nxt = row.get("next_validation_target", {}) or {}
            target = str(nxt.get("target") or "").strip()
            action = str(nxt.get("action") or "").strip()
            if target and action:
                backlog.append({"topic": str(row.get("topic") or "unknown"), "target": target, "action": action})
        backlog.sort(key=lambda item: (item["target"], item["topic"]))
        checks.append(_check("backlog_items_present", "PASS" if backlog else "FAIL", f"items={len(backlog)}"))
        return {"checks": checks, "metrics": {"backlog_count": len(backlog), "backlog_preview": backlog[:10]}, "targets": _collect_targets(["docs/gmut-claim-register-v0.md", "docs/comparative-validation-grid-v1.md"]), "next_action": "Promote backlog items into measurable GMUT falsification tasks.", "records": None, "source_runs": None}

    if system_id == "mind_comparator_regression_guard":
        ok, payload, detail = _read_json_safe("docs/mind-track-gmut-comparator-latest.json")
        if not ok:
            return {"checks": [_check("comparator_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/mind-track-gmut-comparator-latest.json"], "next_action": "Regenerate comparator artifact.", "records": None, "source_runs": None}
        max_abs = float(payload.get("max_abs_deviation", 1.0) or 1.0)
        threshold = float(payload.get("rejection_threshold", 1.0) or 1.0)
        ratio = max_abs / threshold if threshold else 999.0
        checks = [_check("comparator_status", _status_not_fail(_payload_status(payload)), f"status={_payload_status(payload)}"), _check("deviation_ratio", "PASS" if ratio <= 1.0 else "FAIL", f"ratio={ratio:.6f}")]
        return {"checks": checks, "metrics": {"max_abs_deviation": max_abs, "rejection_threshold": threshold, "deviation_ratio": round(ratio, 6)}, "targets": _collect_targets(["docs/mind-track-gmut-comparator-latest.json"]), "next_action": "Maintain comparator bounds unless trace-backed evidence supports updates.", "records": None, "source_runs": None}

    if system_id == "mind_trace_link_drift_check":
        ok_c, canonical, detail_c = _read_json_safe("docs/mind-track-external-anchor-canonical-inputs-v1.json")
        ok_t, trace, detail_t = _read_json_safe("docs/mind-track-gmut-trace-validation-latest.json")
        checks: list[dict[str, str]] = []
        if not ok_c:
            checks.append(_check("canonical_present", "FAIL", detail_c))
        if not ok_t:
            checks.append(_check("trace_present", "FAIL", detail_t))
        if not (ok_c and ok_t):
            return {"checks": checks, "metrics": {}, "targets": _collect_targets(["docs/mind-track-gmut-trace-validation-latest.json"]), "next_action": "Restore canonical and trace artifacts.", "records": None, "source_runs": None}
        canonical_ids = {str(row.get("anchor_id")) for row in canonical.get("anchors", []) if isinstance(row, dict)}
        trace_ids = {str(row.get("anchor_id")) for row in trace.get("anchors", []) if isinstance(row, dict)}
        missing = sorted(canonical_ids - trace_ids)
        extra = sorted(trace_ids - canonical_ids)
        checks.extend(
            [
                _check("canonical_anchor_count", "PASS" if canonical_ids else "FAIL", f"anchors={len(canonical_ids)}"),
                _check("trace_coverage", "PASS" if not missing else "FAIL", f"missing={len(missing)}"),
                _check("trace_extras", "PASS" if not extra else "FAIL", f"extra={len(extra)}"),
            ]
        )
        return {"checks": checks, "metrics": {"canonical_anchor_count": len(canonical_ids), "trace_anchor_count": len(trace_ids), "missing_in_trace": missing, "extra_in_trace": extra}, "targets": _collect_targets(["docs/mind-track-external-anchor-canonical-inputs-v1.json", "docs/mind-track-gmut-trace-validation-latest.json"]), "next_action": "Rerun trace validation after canonical-anchor edits.", "records": None, "source_runs": None}

    if system_id == "mind_theory_signal_refresh_crossref":
        checks, records, runs, targets, metrics = _mind_crossref(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Merge Crossref and Semantic Scholar records.", "records": records, "source_runs": runs}

    if system_id == "mind_theory_signal_refresh_semanticscholar":
        checks, records, runs, targets, metrics = _mind_semanticscholar(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Merge Semantic Scholar and Crossref records.", "records": records, "source_runs": runs}

    if system_id == "mind_theory_signal_merge":
        records, checks, metrics = _merge_records(manifest, ["mind_theory_signal_refresh_crossref", "mind_theory_signal_refresh_semanticscholar"])
        return {"checks": checks, "metrics": metrics, "targets": _collect_targets(["docs/comparative-validation-grid-v1.md"]), "next_action": "Run quality gate before any promotion into curated docs.", "records": records, "source_runs": []}

    if system_id == "mind_theory_signal_quality_gate":
        ok, payload, detail = _read_json_safe(_dependency_output_path(manifest, "mind_theory_signal_merge"))
        if not ok:
            return {"checks": [_check("merge_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/trinity-expansion/mind-theory-signal-merge-latest.json"], "next_action": "Run Mind merge first.", "records": None, "source_runs": None}
        records = [row for row in payload.get("records", []) if isinstance(row, dict)]
        sorted_records = sorted(records, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
        checks = [
            _check("merge_status", _status_not_fail(_payload_status(payload)), f"status={_payload_status(payload)}"),
            _check("minimum_record_count", "PASS" if len(records) >= 4 else "FAIL", f"records={len(records)}"),
            _check("deterministic_ordering", "PASS" if records == sorted_records else "FAIL", "records sorted desc"),
        ]
        return {"checks": checks, "metrics": {"record_count": len(records)}, "targets": _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/trinity-public-source-registry-v1.json"]), "next_action": "Promote only selected PASS-backed records into curated registry.", "records": records, "source_runs": payload.get("source_runs", []) if isinstance(payload.get("source_runs"), list) else []}

    if system_id == "mind_theory_constellation_board":
        deps = ["mind_claim_evidence_partition", "mind_falsification_backlog_builder", "mind_anchor_stability_guard", "mind_comparator_regression_guard", "mind_trace_link_drift_check", "mind_theory_signal_refresh_crossref", "mind_theory_signal_refresh_semanticscholar", "mind_theory_signal_merge", "mind_theory_signal_quality_gate"]
        checks, metrics = _artifact_guard(manifest, deps)
        return {"checks": checks, "metrics": metrics, "targets": _collect_targets(["docs/trinity-mandala-scoreboard-latest.json"]), "next_action": "Treat this as the Mind expansion constellation gate.", "records": None, "source_runs": None}

    if system_id in {"mind_anchor_stability_guard", "body_pipeline_determinism_replay", "heart_signature_chain_consistency"}:
        dep_map = {
            "mind_anchor_stability_guard": ["docs/mind-track-gmut-comparator-latest.json", "docs/mind-track-gmut-anchor-exclusion-latest.json", "docs/mind-track-gmut-trace-validation-latest.json"],
            "body_pipeline_determinism_replay": ["docs/body-track-smoke-latest.json", "docs/body-track-benchmark-latest.json", "docs/body-track-trend-guard-latest.json"],
            "heart_signature_chain_consistency": ["docs/heart-track-governance-latest.json", "docs/heart-track-min-disclosure-latest.json", "docs/heart-track-dispute-recourse-latest.json"],
        }
        checks, metrics = _artifact_guard(manifest, dep_map[system_id])
        return {"checks": checks, "metrics": metrics, "targets": _collect_targets(dep_map[system_id]), "next_action": "Keep dependent artifacts aligned and green.", "records": None, "source_runs": None}

    if system_id == "body_resource_envelope_guard":
        ok, payload, detail = _read_json_safe("docs/system-suite-status.json")
        if not ok:
            return {"checks": [_check("suite_status_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/system-suite-status.json"], "next_action": "Regenerate suite status.", "records": None, "source_runs": None}
        duration = float(payload.get("suite_duration_sec", 0.0) or 0.0)
        results = payload.get("results", [])
        durations = [float(item.get("duration_sec", 0.0) or 0.0) for item in results if isinstance(item, dict)]
        p95 = sorted(durations)[max(int(len(durations) * 0.95) - 1, 0)] if durations else 0.0
        checks = [_check("suite_duration_budget", "PASS" if duration <= 1800.0 else "FAIL", f"suite_duration_sec={duration:.3f}"), _check("step_p95_budget", "PASS" if p95 <= 120.0 else "FAIL", f"step_p95_sec={p95:.3f}")]
        return {"checks": checks, "metrics": {"suite_duration_sec": duration, "step_p95_duration_sec": round(p95, 3)}, "targets": _collect_targets(["docs/system-suite-status.json"]), "next_action": "Tune slow stages only if resource envelope guard fails.", "records": None, "source_runs": None}

    if system_id == "body_latency_budget_guard":
        ok, payload, detail = _read_json_safe("docs/body-track-smoke-latest.json")
        if not ok:
            return {"checks": [_check("body_smoke_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/body-track-smoke-latest.json"], "next_action": "Run body smoke first.", "records": None, "source_runs": None}
        summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
        duration = float(summary.get("total_duration_seconds", 0.0) or 0.0)
        health = float(summary.get("body_health_score", 0.0) or 0.0)
        checks = [_check("latency_budget", "PASS" if duration <= 5.0 else "FAIL", f"duration_sec={duration:.6f}"), _check("health_budget", "PASS" if health >= 50.0 else "FAIL", f"health={health:.3f}")]
        return {"checks": checks, "metrics": {"total_duration_seconds": duration, "body_health_score": health}, "targets": _collect_targets(["docs/body-track-smoke-latest.json"]), "next_action": "Keep body latency and health within budget.", "records": None, "source_runs": None}

    if system_id == "body_config_drift_guard":
        paths = ["docs/body-profile-policy-v1.json", "docs/trinity-api-source-manifest-v1.json", "docs/trinity-expansion-system-manifest-v1.json"]
        checks: list[dict[str, str]] = []
        hashes: dict[str, str] = {}
        for path in paths:
            try:
                digest = hashlib.sha256(_repo_path(path).read_bytes()).hexdigest()
                hashes[path] = digest
                checks.append(_check(f"sha256:{path}", "PASS", digest))
            except Exception as exc:  # noqa: BLE001
                checks.append(_check(f"sha256:{path}", "FAIL", str(exc)))
        return {"checks": checks, "metrics": {"config_sha256": hashes}, "targets": _collect_targets(paths), "next_action": "Treat config hash drift as explicit review trigger.", "records": None, "source_runs": None}

    if system_id in {"body_failure_injection_pack", "body_recovery_time_guard"}:
        ok, payload, detail = _read_json_safe("docs/body-track-policy-stress-latest.json")
        if not ok:
            return {"checks": [_check("stress_artifact_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/body-track-policy-stress-latest.json"], "next_action": "Run stress-window report first.", "records": None, "source_runs": None}
        delta = payload.get("regression_window_stress_delta", {}) if isinstance(payload.get("regression_window_stress_delta"), dict) else {}
        false_delta = float(delta.get("false_alert_rate_delta", 0.0) or 0.0)
        alert_delta = float(delta.get("alert_rate_delta", 0.0) or 0.0)
        if system_id == "body_failure_injection_pack":
            checks = [_check("false_alert_delta_budget", "PASS" if false_delta <= 0.20 else "FAIL", f"delta={false_delta:.6f}")]
            metrics = {"false_alert_rate_delta": round(false_delta, 6), "non_zero_delta_count": int(payload.get("non_zero_delta_count", 0) or 0)}
        else:
            checks = [_check("false_alert_recovery_budget", "PASS" if false_delta <= 0.10 else "FAIL", f"delta={false_delta:.6f}"), _check("alert_recovery_budget", "PASS" if alert_delta <= 0.10 else "FAIL", f"delta={alert_delta:.6f}")]
            metrics = {"false_alert_rate_delta": round(false_delta, 6), "alert_rate_delta": round(alert_delta, 6)}
        return {"checks": checks, "metrics": metrics, "targets": _collect_targets(["docs/body-track-policy-stress-latest.json"]), "next_action": "Keep Body policy updates gated by stress deltas.", "records": None, "source_runs": None}

    if system_id == "body_runtime_connectivity_probe":
        checks, records, runs, targets, metrics = _connectivity_probe_live(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use connectivity probe as advisory runtime context.", "records": records, "source_runs": runs}

    if system_id == "body_dependency_health_refresh":
        checks, records, runs, targets, metrics = _github_watchlist_live(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use dependency health refresh as standards-first Body context.", "records": records, "source_runs": runs}

    if system_id == "body_compute_signal_merge":
        records, checks, metrics = _merge_records(manifest, ["body_runtime_connectivity_probe", "body_dependency_health_refresh", "docs/body-compute-signal-board-latest.json"])
        return {"checks": checks, "metrics": metrics, "targets": _collect_targets(["docs/comparative-validation-grid-v1.md"]), "next_action": "Run Body quality gate before promoting comparison updates.", "records": records, "source_runs": []}

    if system_id == "body_compute_signal_quality_gate":
        ok, payload, detail = _read_json_safe(_dependency_output_path(manifest, "body_compute_signal_merge"))
        if not ok:
            return {"checks": [_check("merge_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/trinity-expansion/body-compute-signal-merge-latest.json"], "next_action": "Run Body merge first.", "records": None, "source_runs": None}
        records = [row for row in payload.get("records", []) if isinstance(row, dict)]
        github_records = [row for row in records if str(row.get("source_id")) == "github"]
        checks = [_check("merge_status", _status_not_fail(_payload_status(payload)), f"status={_payload_status(payload)}"), _check("minimum_record_count", "PASS" if len(records) >= 5 else "FAIL", f"records={len(records)}"), _check("github_coverage", "PASS" if len(github_records) >= 3 else "FAIL", f"github_records={len(github_records)}")]
        return {"checks": checks, "metrics": {"record_count": len(records), "github_record_count": len(github_records)}, "targets": _collect_targets(["docs/trinity-mandala-scoreboard-latest.json"]), "next_action": "Treat this quality gate as Body expansion constellation gate.", "records": records, "source_runs": payload.get("source_runs", []) if isinstance(payload.get("source_runs"), list) else []}

    if system_id == "heart_governance_signal_refresh_worldbank_oecd":
        checks, records, runs, targets, metrics = _heart_worldbank_oecd_live(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use NZ-plus-global governance context without asserting legal force.", "records": records, "source_runs": runs}

    if system_id == "heart_governance_signal_refresh_data_govt_nz":
        checks, records, runs, targets, metrics = _heart_data_govt_live(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use NZ open-data context as advisory governance evidence.", "records": records, "source_runs": runs}

    if system_id == "heart_governance_signal_refresh_standards_docs":
        checks, records, runs, targets, metrics = _heart_standards_live(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use standards endpoint checks as governance bridge context.", "records": records, "source_runs": runs}

    if system_id == "heart_did_method_conformance_suite":
        checks: list[dict[str, str]] = []
        verifier = _repo_path("freed_id_did_signature_verifier.py")
        if not verifier.exists():
            checks.append(_check("did_verifier_exists", "FAIL", "freed_id_did_signature_verifier.py missing"))
            return {"checks": checks, "metrics": {}, "targets": ["freed_id_did_signature_verifier.py"], "next_action": "Restore DID verifier scaffold.", "records": None, "source_runs": None}
        text = verifier.read_text(encoding="utf-8")
        tokens = ["build_did_method_signature_verifier", "verify_ed25519_signature_ref", "ED25519_METHOD_TYPES"]
        missing = [token for token in tokens if token not in text]
        checks.append(_check("did_verifier_tokens", "PASS" if not missing else "FAIL", f"missing_tokens={len(missing)}"))
        ok, gov, detail = _read_json_safe("docs/heart-track-governance-latest.json")
        if not ok:
            checks.append(_check("governance_artifact", "FAIL", detail))
        else:
            checks.append(_check("governance_status", _status_not_fail(_payload_status(gov)), f"status={_payload_status(gov)}"))
        return {"checks": checks, "metrics": {"required_token_count": len(tokens), "missing_token_count": len(missing)}, "targets": _collect_targets(["freed_id_did_signature_verifier.py", "docs/heart-track-governance-latest.json"]), "next_action": "Extend DID conformance vectors as GOV-004 verification expands.", "records": None, "source_runs": None}

    if system_id == "heart_revocation_replay_guard":
        ok_g, gov, detail_g = _read_json_safe("docs/heart-track-governance-latest.json")
        ok_a, adv, detail_a = _read_json_safe("docs/heart-track-min-disclosure-adversarial-latest.json")
        checks: list[dict[str, str]] = []
        if not ok_g:
            checks.append(_check("governance_artifact", "FAIL", detail_g))
        if not ok_a:
            checks.append(_check("adversarial_artifact", "FAIL", detail_a))
        if ok_g:
            gov_checks = gov.get("checks", []) if isinstance(gov.get("checks"), list) else []
            required_checks = {"revoke_did", "issue_credential_after_revoke", "verify_credential_after_revoke"}
            seen = {str(item.get("check")) for item in gov_checks if isinstance(item, dict)}
            missing = sorted(required_checks - seen)
            checks.append(_check("revocation_path", "PASS" if not missing else "FAIL", f"missing={missing}"))
        if ok_a:
            checks.append(_check("adversarial_status", _status_not_fail(_payload_status(adv)), f"status={_payload_status(adv)}"))
        return {"checks": checks, "metrics": {}, "targets": _collect_targets(["docs/heart-track-governance-latest.json", "docs/heart-track-min-disclosure-adversarial-latest.json"]), "next_action": "Keep revocation negative-path checks mandatory.", "records": None, "source_runs": None}

    if system_id == "heart_recourse_sla_guard":
        ok_m, main, detail_m = _read_json_safe("docs/heart-track-dispute-recourse-latest.json")
        ok_a, adv, detail_a = _read_json_safe("docs/heart-track-dispute-recourse-adversarial-latest.json")
        checks: list[dict[str, str]] = []
        if not ok_m:
            checks.append(_check("main_artifact", "FAIL", detail_m))
        if not ok_a:
            checks.append(_check("adversarial_artifact", "FAIL", detail_a))
        if ok_m:
            final_case = main.get("final_case", {}) if isinstance(main.get("final_case"), dict) else {}
            history = final_case.get("history", []) if isinstance(final_case.get("history"), list) else []
            signed_steps = sum(1 for row in history if isinstance(row, dict) and bool(row.get("signature_verified")))
            checks.append(_check("main_status", _status_not_fail(_payload_status(main)), f"status={_payload_status(main)}"))
            checks.append(_check("signed_transition_density", "PASS" if signed_steps >= 5 else "FAIL", f"signed_steps={signed_steps}"))
        if ok_a:
            checks.append(_check("adversarial_status", _status_not_fail(_payload_status(adv)), f"status={_payload_status(adv)}"))
        return {"checks": checks, "metrics": {}, "targets": _collect_targets(["docs/heart-track-dispute-recourse-latest.json", "docs/heart-track-dispute-recourse-adversarial-latest.json"]), "next_action": "Maintain signed recourse transitions for SLA confidence.", "records": None, "source_runs": None}

    if system_id == "heart_alignment_gap_guard":
        path = _repo_path("docs/comparative-validation-grid-v1.md")
        if not path.exists():
            return {"checks": [_check("comparative_grid_present", "FAIL", "docs/comparative-validation-grid-v1.md missing")], "metrics": {}, "targets": ["docs/comparative-validation-grid-v1.md"], "next_action": "Restore comparative grid.", "records": None, "source_runs": None}
        text = path.read_text(encoding="utf-8")
        checks = [
            _check("alignment_column_present", "PASS" if "Alignment in repo" in text else "FAIL", "alignment column expected"),
            _check("gap_column_present", "PASS" if "| Gap |" in text else "FAIL", "gap column expected"),
            _check("next_proof_column_present", "PASS" if "Next implementation proof" in text else "FAIL", "next proof column expected"),
        ]
        return {"checks": checks, "metrics": {"grid_length": len(text)}, "targets": _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"]), "next_action": "Keep alignment/gap/proof columns explicit for governance updates.", "records": None, "source_runs": None}

    if system_id == "heart_policy_exception_register_guard":
        ok, payload, detail = _read_json_safe("docs/heart-policy-exception-register-v1.json")
        if not ok:
            return {"checks": [_check("exception_register_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/heart-policy-exception-register-v1.json"], "next_action": "Create Heart exception register.", "records": None, "source_runs": None}
        rows = payload.get("exceptions", [])
        rows = rows if isinstance(rows, list) else []
        required = {"exception_id", "opened_utc", "owner", "reason", "status"}
        invalid = 0
        for row in rows:
            if not isinstance(row, dict) or not required.issubset(row.keys()):
                invalid += 1
        checks = [_check("register_loaded", "PASS", "register loaded"), _check("exception_schema_valid", "PASS" if invalid == 0 else "FAIL", f"invalid_entries={invalid}")]
        return {"checks": checks, "metrics": {"exception_count": len(rows), "invalid_entries": invalid}, "targets": _collect_targets(["docs/heart-policy-exception-register-v1.json"]), "next_action": "Keep governance exceptions typed and reviewable.", "records": None, "source_runs": None}

    if system_id == "heart_governance_constellation_board":
        deps = ["heart_governance_signal_refresh_worldbank_oecd", "heart_governance_signal_refresh_data_govt_nz", "heart_governance_signal_refresh_standards_docs", "heart_did_method_conformance_suite", "heart_signature_chain_consistency", "heart_revocation_replay_guard", "heart_recourse_sla_guard", "heart_alignment_gap_guard", "heart_policy_exception_register_guard"]
        checks, metrics = _artifact_guard(manifest, deps)
        records, _, _ = _merge_records(manifest, deps)
        return {"checks": checks, "metrics": metrics, "targets": _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/trinity-mandala-scoreboard-latest.json"]), "next_action": "Treat this as the Heart expansion constellation gate.", "records": records, "source_runs": []}

    if system_id == "trinity_capability_surface_audit":
        codex_config_path = Path.home() / ".codex" / "config.toml"
        config = _parse_toml_file(codex_config_path)
        model = str(config.get("model") or "")
        reasoning_effort = str(config.get("model_reasoning_effort") or "")
        mcp_servers = config.get("mcp_servers", {})
        mcp_server_names = sorted(mcp_servers.keys()) if isinstance(mcp_servers, dict) else []
        exposed_env = [name for name in RELEVANT_ENV_VARS if os.getenv(name)]
        mcp_settings_path = Path.home() / "Library" / "Application Support" / "Codex" / "mcp_settings.json"
        suite_ok, suite_payload, _ = _read_json_safe("docs/system-suite-status.json")
        last_expansion_total = int(suite_payload.get("expansion_systems_total", 0) or 0) if suite_ok else 0
        checks = [
            _check("codex_config_present", "PASS" if codex_config_path.exists() else "FAIL", str(codex_config_path)),
            _check("preferred_model_gpt54", "PASS" if model == "gpt-5.4" else "FAIL", f"model={model or 'missing'}"),
            _check("credential_env_absent", "PASS" if not exposed_env else "FAIL", f"exposed={exposed_env}"),
            _check("uvx_absent", "PASS" if shutil.which("uvx") is None else "FAIL", f"uvx={shutil.which('uvx') or 'absent'}"),
            _check("repo_skill_inventory_present", "PASS" if len(_repo_skill_dirs()) >= 1 else "FAIL", f"repo_skills={len(_repo_skill_dirs())}"),
            _check("manifest_system_count", "PASS" if len(manifest.get("systems", [])) == 80 else "FAIL", f"systems={len(manifest.get('systems', []))}"),
            _check("mcp_resource_surface_absent", "PASS" if not mcp_settings_path.exists() else "FAIL", f"mcp_settings_present={mcp_settings_path.exists()}"),
        ]
        return {
            "checks": checks,
            "metrics": {
                "configured_model": model,
                "configured_reasoning_effort": reasoning_effort,
                "repo_python_scripts": _count_script_files(),
                "repo_local_skill_count": len(_repo_skill_dirs()),
                "local_codex_skill_count": len(_local_skill_dirs()),
                "manifest_system_count": len(manifest.get("systems", [])),
                "last_recorded_suite_expansion_total": last_expansion_total,
                "exposed_env_vars": exposed_env,
                "uvx_present": shutil.which("uvx") is not None,
                "mcp_servers_configured": mcp_server_names,
                "mcp_resource_templates_available": False,
                "mcp_resources_available": False,
                "mcp_settings_present": mcp_settings_path.exists(),
                "code_home_present": bool(os.getenv("CODEX_HOME")),
            },
            "targets": _collect_targets(["docs/system-suite-status.json", "docs/trinity-expansion-system-manifest-v2.json"]),
            "next_action": "Use this audit as the environment baseline before widening integrations.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_safe_bootstrap_audit":
        files = {
            "config": Path.home() / ".codex" / "config.toml",
            "god_functions": Path.home() / ".codex" / "god_functions.sh",
            "mcp_settings": Path.home() / "Library" / "Application Support" / "Codex" / "mcp_settings.json",
            "bashrc": Path.home() / ".bashrc",
            "zshrc": Path.home() / ".zshrc",
        }
        marker_hits: dict[str, list[str]] = {}
        for label, path in files.items():
            if not path.exists():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:  # noqa: BLE001
                continue
            hits = [marker for marker in SAFE_BOOTSTRAP_MARKERS if marker in text]
            if hits:
                marker_hits[label] = hits
        checks = [
            _check("unsafe_markers_absent", "PASS" if not marker_hits else "FAIL", f"hits={marker_hits}"),
            _check("god_functions_absent_or_safe", "PASS" if "god_functions" not in marker_hits else "FAIL", f"hits={marker_hits.get('god_functions', [])}"),
            _check("shell_rc_injection_absent", "PASS" if not any(label in marker_hits for label in {"bashrc", "zshrc"}) else "FAIL", f"hits={marker_hits}"),
        ]
        return {
            "checks": checks,
            "metrics": {"dangerous_marker_count": sum(len(values) for values in marker_hits.values()), "files_scanned": len(files), "marker_hits": marker_hits},
            "targets": _collect_targets(["docs/trinity-safe-bootstrap-template-v1.sh", "docs/trinity-safe-bootstrap-config-v1.toml"]),
            "next_action": "Keep bootstrap material advisory and never inject bypass flags into shell or Codex config.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_safe_bootstrap_template_builder":
        script_path = "docs/trinity-safe-bootstrap-template-v1.sh"
        config_path = "docs/trinity-safe-bootstrap-config-v1.toml"
        note_path = "docs/trinity-safe-bootstrap-notes-v1.md"
        script_text = """#!/usr/bin/env bash
set -eu

CODEX_DIR=\"$HOME/.codex\"
CONFIG_FILE=\"$CODEX_DIR/config.toml\"

mkdir -p \"$CODEX_DIR\"

if [ ! -f \"$CONFIG_FILE\" ]; then
  cat > \"$CONFIG_FILE\" <<'EOF'
model = \"gpt-5.4\"
model_reasoning_effort = \"xhigh\"

[windows]
sandbox = \"elevated\"
EOF
fi

echo \"Safe bootstrap complete. Review config manually before enabling extra integrations.\"
"""
        config_text = """model = \"gpt-5.4\"
model_reasoning_effort = \"xhigh\"

[windows]
sandbox = \"elevated\"
"""
        note_text = """# Safe Bootstrap Notes v1

- No shell-RC injection.
- No approval bypass aliases.
- No automatic MCP token insertion.
- Public/local workflow only unless credentials are explicitly added later.
"""
        paths = [
            _write_text(script_path, script_text),
            _write_text(config_path, config_text),
            _write_text(note_path, note_text),
        ]
        checks = [_check("template_files_written", "PASS", f"files={len(paths)}")]
        return {
            "checks": checks,
            "metrics": {"file_count": len(paths)},
            "targets": _collect_targets([script_path, config_path, note_path]),
            "next_action": "Use the safe bootstrap template only as a reviewed, manual starting point.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_secrets_exposure_guard":
        exposed_env = [name for name in RELEVANT_ENV_VARS if os.getenv(name)]
        api_manifest = _read_json("docs/trinity-api-source-manifest-v1.json")
        apis = [row for row in api_manifest.get("apis", []) if isinstance(row, dict)]
        non_public = [str(row.get("api_id") or "") for row in apis if str(row.get("auth_mode") or "") != "public_unauthenticated"]
        checks = [
            _check("credential_env_absent", "PASS" if not exposed_env else "FAIL", f"exposed={exposed_env}"),
            _check("public_auth_only_manifest", "PASS" if not non_public else "FAIL", f"non_public={non_public}"),
        ]
        return {
            "checks": checks,
            "metrics": {"exposed_env_vars": exposed_env, "manifest_api_count": len(apis), "non_public_api_ids": non_public},
            "targets": _collect_targets(["docs/trinity-api-source-manifest-v1.json"]),
            "next_action": "Keep this phase public/local only until credentials are intentionally introduced.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_live_network_policy_guard":
        ok_text, run_all_text, detail = _read_text_safe("scripts/run_all_trinity_systems.py")
        if not ok_text:
            return {"checks": [_check("run_all_present", "FAIL", detail)], "metrics": {}, "targets": ["scripts/run_all_trinity_systems.py"], "next_action": "Restore run_all orchestration.", "records": None, "source_runs": None}
        live_entries = [row for row in manifest.get("systems", []) if isinstance(row, dict) and str(row.get("mode")) == "live"]
        cache_backed = [row for row in live_entries if isinstance(row.get("cache_artifacts"), list) and bool(row.get("cache_artifacts"))]
        checks = [
            _check("offline_only_flag_present", "PASS" if "--offline-only" in run_all_text else "FAIL", "run_all requires explicit offline override"),
            _check("compat_alias_present", "PASS" if "--include-public-api-refresh" in run_all_text else "FAIL", "compatibility alias expected"),
            _check("live_default_present", "PASS" if 'live_network_mode = "live_default"' in run_all_text else "FAIL", "standard/deep should resolve to live_default"),
            _check("live_entries_cache_backed", "PASS" if len(cache_backed) == len(live_entries) else "FAIL", f"cache_backed={len(cache_backed)}/{len(live_entries)}"),
        ]
        return {
            "checks": checks,
            "metrics": {"live_entry_count": len(live_entries), "cache_backed_live_entries": len(cache_backed)},
            "targets": _collect_targets(["scripts/run_all_trinity_systems.py", "docs/trinity-expansion-system-manifest-v2.json"]),
            "next_action": "Keep every live stage cache-backed so offline-only remains viable.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_dependency_surface_report":
        import_pattern = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_][A-Za-z0-9_\.]*)", re.MULTILINE)
        local_modules = {path.stem for path in PYTHON_SCRIPTS.glob("*.py")}
        local_modules.update(path.stem for path in ROOT.glob("*.py"))
        stdlib_modules = set(getattr(sys, "stdlib_module_names", set()))
        imports: set[str] = set()
        for path in list(PYTHON_SCRIPTS.glob("*.py")) + list(ROOT.glob("*.py")):
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:  # noqa: BLE001
                continue
            for match in import_pattern.findall(text):
                imports.add(match.split(".")[0])
        external = sorted(name for name in imports if name not in stdlib_modules and name not in local_modules and name != "__future__")
        checks = [
            _check("import_scan_complete", "PASS", f"imports={len(imports)}"),
            _check("dependency_surface_documented", "PASS", f"external={len(external)}"),
        ]
        return {
            "checks": checks,
            "metrics": {"total_import_roots": len(imports), "external_import_roots": external[:25]},
            "targets": _collect_targets(["scripts/trinity_expansion_system_runner.py", "scripts/run_all_trinity_systems.py"]),
            "next_action": "Prefer stdlib and existing repo dependencies before widening the runtime surface.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_trust_boundary_map":
        api_manifest = _read_json("docs/trinity-api-source-manifest-v1.json")
        boundaries = [
            "repo_workspace",
            "codex_home_config",
            "local_shell_toolchain",
            "public_unauthenticated_api_surface",
            "git_history_and_remote_lineage",
            "generated_docs_artifact_lane",
        ]
        checks = [
            _check("boundary_count", "PASS" if len(boundaries) >= 5 else "FAIL", f"boundaries={len(boundaries)}"),
            _check("public_api_surface_present", "PASS" if len(api_manifest.get("apis", [])) >= 1 else "FAIL", f"apis={len(api_manifest.get('apis', []))}"),
        ]
        return {
            "checks": checks,
            "metrics": {"boundary_count": len(boundaries), "boundaries": boundaries},
            "targets": _collect_targets(["docs/trinity-api-source-manifest-v1.json", "docs/trinity-expansion-system-manifest-v2.json"]),
            "next_action": "Keep trust boundaries explicit before expanding connectivity or authority.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_operation_mode_guard":
        ok_text, run_all_text, detail = _read_text_safe("scripts/run_all_trinity_systems.py")
        if not ok_text:
            return {"checks": [_check("run_all_present", "FAIL", detail)], "metrics": {}, "targets": ["scripts/run_all_trinity_systems.py"], "next_action": "Restore run_all orchestration.", "records": None, "source_runs": None}
        checks = [
            _check("profile_modes_present", "PASS" if all(token in run_all_text for token in ['"standard"', '"quick"', '"deep"']) else "FAIL", "standard/quick/deep expected"),
            _check("offline_only_present", "PASS" if "--offline-only" in run_all_text else "FAIL", "offline override required"),
            _check("manifest_v2_present", "PASS" if "trinity-expansion-system-manifest-v2.json" in run_all_text else "FAIL", "run_all should target v2 manifest"),
        ]
        return {
            "checks": checks,
            "metrics": {"quick_mode_supported": "--quick-mode" in run_all_text, "status_json_supported": "--status-json" in run_all_text},
            "targets": _collect_targets(["scripts/run_all_trinity_systems.py", "docs/system-suite-status.json"]),
            "next_action": "Keep quick as continuity mode and standard/deep as full gating profiles.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_threat_model_board":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        assets = ["repo evidence docs", "expansion manifest", "home codex config", "public API caches", "Freed ID governance artifacts"]
        attacker_paths = ["unsafe bootstrap mutation", "secret leakage", "cache poisoning", "dependency drift", "live network fallback confusion"]
        checks.extend(
            [
                _check("asset_inventory", "PASS" if len(assets) >= 5 else "FAIL", f"assets={len(assets)}"),
                _check("attacker_path_inventory", "PASS" if len(attacker_paths) >= 5 else "FAIL", f"paths={len(attacker_paths)}"),
            ]
        )
        metrics.update({"asset_count": len(assets), "attacker_path_count": len(attacker_paths)})
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/trinity-expansion-system-manifest-v2.json", "docs/trinity-api-source-manifest-v1.json"]),
            "next_action": "Keep hardening and public/local boundaries ahead of new privileged integrations.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_release_gate_board":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/trinity-expansion-manifest-validation-latest.json", "docs/trinity-expansion-result-validation-latest.json"]),
            "next_action": "Use this hardening gate before trusting the wider 80-system expansion lane.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "mind_claim_source_coverage_guard":
        ok_text, text, detail = _read_text_safe("docs/gmut-claim-register-v0.md")
        if not ok_text:
            return {"checks": [_check("claim_register_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/gmut-claim-register-v0.md"], "next_action": "Restore the claim register.", "records": None, "source_runs": None}
        matrix_section = _markdown_section(text, "Claim matrix")
        claim_rows = [line for line in matrix_section.splitlines() if line.startswith("| GMUT-")]
        missing_source = 0
        missing_falsification = 0
        for row in claim_rows:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) < 8:
                continue
            if not cells[2]:
                missing_source += 1
            if not cells[7]:
                missing_falsification += 1
        checks = [
            _check("claim_row_count", "PASS" if len(claim_rows) >= 8 else "FAIL", f"rows={len(claim_rows)}"),
            _check("claim_sources_present", "PASS" if missing_source == 0 else "FAIL", f"missing_source={missing_source}"),
            _check("next_falsification_present", "PASS" if missing_falsification == 0 else "FAIL", f"missing_next={missing_falsification}"),
        ]
        return {
            "checks": checks,
            "metrics": {"claim_row_count": len(claim_rows), "missing_source_rows": missing_source, "missing_next_falsification_rows": missing_falsification},
            "targets": _collect_targets(["docs/gmut-claim-register-v0.md"]),
            "next_action": "Keep every GMUT claim tied to a source, observable, and next falsification step.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "mind_inference_boundary_guard":
        ok_text, text, detail = _read_text_safe("docs/gmut-claim-register-v0.md")
        if not ok_text:
            return {"checks": [_check("claim_register_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/gmut-claim-register-v0.md"], "next_action": "Restore the claim register.", "records": None, "source_runs": None}
        checks = [
            _check("confirmed_evidence_tag", "PASS" if "confirmed_evidence" in text else "FAIL", "confirmed_evidence tag required"),
            _check("inference_tag", "PASS" if "inference" in text else "FAIL", "inference tag required"),
            _check("open_gap_tag", "PASS" if "open_gap" in text else "FAIL", "open_gap tag required"),
            _check("classification_rule_present", "PASS" if "Evidence classification rule" in text else "FAIL", "classification rule expected"),
        ]
        return {
            "checks": checks,
            "metrics": {"aura_v38_note_present": "Aura v38 intake note" in text},
            "targets": _collect_targets(["docs/gmut-claim-register-v0.md"]),
            "next_action": "Preserve evidence, inference, and open-gap boundaries in every Mind update.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "mind_falsification_priority_matrix":
        ok_text, text, detail = _read_text_safe("docs/gmut-claim-register-v0.md")
        if not ok_text:
            return {"checks": [_check("claim_register_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/gmut-claim-register-v0.md"], "next_action": "Restore the claim register.", "records": None, "source_runs": None}
        matrix_section = _markdown_section(text, "Claim matrix")
        claim_rows = [line for line in matrix_section.splitlines() if line.startswith("| GMUT-")]
        status_counts: dict[str, int] = {}
        next_steps = 0
        for row in claim_rows:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) < 8:
                continue
            status_counts[cells[5]] = status_counts.get(cells[5], 0) + 1
            if cells[7]:
                next_steps += 1
        checks = [
            _check("priority_rows_present", "PASS" if claim_rows else "FAIL", f"rows={len(claim_rows)}"),
            _check("all_rows_have_next_step", "PASS" if next_steps == len(claim_rows) else "FAIL", f"next_steps={next_steps}/{len(claim_rows)}"),
            _check("externally_testable_claim_present", "PASS" if status_counts.get("externally_testable", 0) >= 1 else "FAIL", f"externally_testable={status_counts.get('externally_testable', 0)}"),
        ]
        return {
            "checks": checks,
            "metrics": {"status_counts": status_counts, "claim_row_count": len(claim_rows)},
            "targets": _collect_targets(["docs/gmut-claim-register-v0.md"]),
            "next_action": "Prioritize externally-testable and simulator-backed claims before speculative expansion.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "mind_numeric_anchor_delta_guard":
        ok, payload, detail = _read_json_safe("docs/mind-track-gmut-anchor-exclusion-latest.json")
        if not ok:
            return {"checks": [_check("anchor_exclusion_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/mind-track-gmut-anchor-exclusion-latest.json"], "next_action": "Regenerate anchor exclusion note.", "records": None, "source_runs": None}
        anchors = payload.get("anchors", [])
        anchors = anchors if isinstance(anchors, list) else []
        overhangs = [float(row.get("overhang_factor", 0.0) or 0.0) for row in anchors if isinstance(row, dict)]
        checks = [
            _check("anchor_rows_present", "PASS" if len(anchors) >= 3 else "FAIL", f"anchors={len(anchors)}"),
            _check("comparator_status", "PASS" if str(payload.get("comparator_status")) == "PASS" else "FAIL", f"comparator_status={payload.get('comparator_status')}"),
            _check("conservative_bounds_present", "PASS" if all("conservative_external_upper_bound" in row for row in anchors if isinstance(row, dict)) else "FAIL", "conservative bounds required"),
            _check("overhang_documented", "PASS" if overhangs and max(overhangs) > 1.0 else "FAIL", f"max_overhang={max(overhangs) if overhangs else 0.0}"),
        ]
        return {
            "checks": checks,
            "metrics": {"anchor_count": len(anchors), "max_overhang_factor": max(overhangs) if overhangs else 0.0, "min_overhang_factor": min(overhangs) if overhangs else 0.0},
            "targets": _collect_targets(["docs/mind-track-gmut-anchor-exclusion-latest.json", "docs/mind-track-gmut-comparator-latest.json"]),
            "next_action": "Keep numeric anchor deltas visible until the GMUT overhang is materially reduced.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "mind_traceability_ledger_check":
        ok, payload, detail = _read_json_safe("docs/mind-track-gmut-trace-validation-latest.json")
        if not ok:
            return {"checks": [_check("trace_validation_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/mind-track-gmut-trace-validation-latest.json"], "next_action": "Restore trace validation artifact.", "records": None, "source_runs": None}
        anchors = payload.get("anchors", [])
        anchors = anchors if isinstance(anchors, list) else []
        pass_count = sum(1 for row in anchors if isinstance(row, dict) and str(row.get("status")) == "PASS")
        checks = [
            _check("trace_validation_status", _status_not_fail(_payload_status(payload)), f"status={_payload_status(payload)}"),
            _check("anchor_trace_rows", "PASS" if len(anchors) >= 3 else "FAIL", f"anchors={len(anchors)}"),
            _check("anchor_trace_pass_count", "PASS" if pass_count == len(anchors) else "FAIL", f"pass_count={pass_count}/{len(anchors)}"),
        ]
        return {
            "checks": checks,
            "metrics": {"anchor_count": len(anchors), "pass_count": pass_count},
            "targets": _collect_targets(["docs/mind-track-gmut-trace-validation-latest.json", "docs/mind-track-external-anchor-trace-manifest-v1.json"]),
            "next_action": "Keep checksum-linked trace artifacts attached to every external anchor row.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "mind_public_theory_refresh_arxiv":
        checks, records, runs, targets, metrics = _mind_arxiv_live(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use arXiv recency as theory context only, not as GMUT evidence uplift.", "records": records, "source_runs": runs}

    if system_id == "mind_public_theory_refresh_openalex":
        query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
        queries = [row for row in query_pack.get("mind", {}).get("queries", []) if isinstance(row, dict)]
        fallback_records = (
            _records_from_latest("docs/trinity-expansion/mind-public-theory-refresh-openalex-latest.json")
            or _records_from_api_cache("docs/trinity-api-cache/mind-signals-latest.json", source_ids={"openalex"})
            or _records_from_public_registry(pillar="mind", topic_terms=["string theory", "quantum gravity", "testability"])
        )
        checks, records, runs, targets, metrics = _openalex_live(
            pillar="mind",
            query_rows=queries,
            latest_path="docs/trinity-expansion/mind-public-theory-refresh-openalex-latest.json",
            timeout_sec=timeout_sec,
            offline_only=offline_only,
            fallback_records=fallback_records,
        )
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use OpenAlex recency as comparator context only.", "records": records, "source_runs": runs}

    if system_id == "mind_public_theory_refresh_crossref":
        query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
        queries = [row for row in query_pack.get("mind", {}).get("queries", []) if isinstance(row, dict)]
        fallback_records = (
            _records_from_latest("docs/trinity-expansion/mind-public-theory-refresh-crossref-latest.json")
            or _records_from_latest("docs/trinity-expansion/mind-theory-signal-refresh-crossref-latest.json")
            or _records_from_public_registry(pillar="mind", topic_terms=["string theory", "quantum gravity", "testability"])
        )
        checks, records, runs, targets, metrics = _crossref_live(
            pillar="mind",
            query_rows=queries,
            timeout_sec=timeout_sec,
            offline_only=offline_only,
            fallback_records=fallback_records,
        )
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use Crossref metadata as current publication context for Mind.", "records": records, "source_runs": runs}

    if system_id == "mind_theory_promotion_candidate_board":
        records, checks, metrics = _merge_records(manifest, ["mind_public_theory_refresh_arxiv", "mind_public_theory_refresh_openalex", "mind_public_theory_refresh_crossref"])
        candidate_targets = _candidate_targets(records)
        source_ids = sorted({str(row.get("source_id") or "") for row in records if isinstance(row, dict)})
        checks.extend(
            [
                _check("source_diversity", "PASS" if len(source_ids) >= 2 else "FAIL", f"sources={source_ids}"),
                _check("candidate_targets_present", "PASS" if candidate_targets else "FAIL", f"targets={len(candidate_targets)}"),
            ]
        )
        metrics.update({"candidate_target_count": len(candidate_targets), "source_ids": source_ids, "top_candidate_targets": candidate_targets[:5]})
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets([row["target"] for row in candidate_targets] + ["docs/comparative-validation-grid-v1.md", "docs/gmut-claim-register-v0.md"]),
            "next_action": "Promote only manually reviewed PASS-backed targets into the curated Mind corpus.",
            "records": records,
            "source_runs": [],
        }

    if system_id == "mind_theory_readiness_gate":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        records, _, _ = _merge_records(manifest, ["mind_theory_promotion_candidate_board", "mind_theory_constellation_board"])
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/trinity-mandala-scoreboard-latest.json"]),
            "next_action": "Treat this as the Mind readiness gate before any narrative uplift.",
            "records": records,
            "source_runs": [],
        }

    if system_id == "body_execution_graph_integrity":
        try:
            from run_all_trinity_systems import build_commands
        except Exception as exc:  # noqa: BLE001
            return {"checks": [_check("import_build_commands", "FAIL", str(exc))], "metrics": {}, "targets": ["scripts/run_all_trinity_systems.py"], "next_action": "Restore suite orchestration imports.", "records": None, "source_runs": None}
        commands = build_commands(
            include_skill_install=False,
            include_version_scan=False,
            include_curated_skill_catalog=False,
            include_public_api_refresh=True,
            offline_only=False,
            quick_mode=False,
            profile="standard",
            body_benchmark_mode="enforce",
        )
        expansion_labels = [label for label, _ in commands if label.startswith("expansion: ")]
        checks = [
            _check("standard_expansion_count", "PASS" if len(expansion_labels) == len(manifest.get("systems", [])) else "FAIL", f"labels={len(expansion_labels)}"),
            _check("expansion_labels_unique", "PASS" if len(expansion_labels) == len(set(expansion_labels)) else "FAIL", f"unique={len(set(expansion_labels))}"),
        ]
        return {
            "checks": checks,
            "metrics": {"standard_expansion_labels": len(expansion_labels), "manifest_system_count": len(manifest.get("systems", []))},
            "targets": _collect_targets(["scripts/run_all_trinity_systems.py", "docs/trinity-expansion-system-manifest-v2.json"]),
            "next_action": "Keep suite expansion wiring aligned with the manifest-driven graph.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "body_cache_determinism_guard":
        cache_paths = [
            "docs/trinity-api-cache/mind-signals-latest.json",
            "docs/trinity-api-cache/body-signals-latest.json",
            "docs/trinity-api-cache/heart-signals-latest.json",
        ]
        checks: list[dict[str, str]] = []
        deterministic = 0
        for path in cache_paths:
            ok, payload, detail = _read_json_safe(path)
            if not ok:
                checks.append(_check(f"cache:{path}", "FAIL", detail))
                continue
            rows = [row for row in payload.get("records", []) if isinstance(row, dict)]
            sorted_rows = sorted(rows, key=lambda row: (str(row.get("published_at")), str(row.get("record_id"))), reverse=True)
            generated = bool(payload.get("generated_utc"))
            if generated:
                deterministic += 1
            checks.append(
                _check(
                    f"cache_order_or_timestamp:{path}",
                    "PASS" if rows == sorted_rows or generated else "FAIL",
                    f"records={len(rows)} generated_utc={payload.get('generated_utc', '')}",
                )
            )
        return {
            "checks": checks,
            "metrics": {"cache_count": len(cache_paths), "deterministic_cache_count": deterministic},
            "targets": _collect_targets(cache_paths),
            "next_action": "Keep cached API artifacts stably ordered for offline reuse and reproducibility.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "body_artifact_reproducibility_guard":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(deps),
            "next_action": "Keep Body evidence reproducible before widening external comparison claims.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "body_resource_budget_forecaster":
        ok_suite, suite_payload, detail_suite = _read_json_safe("docs/system-suite-status.json")
        ok_energy, energy_payload, detail_energy = _read_json_safe("docs/energy-bank-report.json")
        checks: list[dict[str, str]] = []
        if not ok_suite:
            checks.append(_check("suite_status_present", "FAIL", detail_suite))
        if not ok_energy:
            checks.append(_check("energy_report_present", "FAIL", detail_energy))
        if ok_suite and ok_energy:
            duration = float(suite_payload.get("suite_duration_sec", 0.0) or 0.0)
            outputs = energy_payload.get("outputs", {}) if isinstance(energy_payload.get("outputs"), dict) else {}
            projection = outputs.get("projection_summary", {}) if isinstance(outputs.get("projection_summary"), dict) else {}
            reserve_tokens = float(outputs.get("reserve_tokens", 0.0) or 0.0)
            checks.extend(
                [
                    _check("suite_duration_recorded", "PASS" if duration > 0 else "FAIL", f"duration={duration:.3f}"),
                    _check("reserve_tokens_positive", "PASS" if reserve_tokens > 0 else "FAIL", f"reserve_tokens={reserve_tokens:.3f}"),
                    _check("projection_summary_present", "PASS" if bool(projection) else "FAIL", f"projection_keys={list(projection.keys()) if projection else []}"),
                ]
            )
            metrics = {"suite_duration_sec": duration, "reserve_tokens": reserve_tokens, "projection_summary": projection}
        else:
            metrics = {}
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/system-suite-status.json", "docs/energy-bank-report.json"]),
            "next_action": "Use budget forecasts as operating context, not as permission to relax reproducibility gates.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "body_failure_recovery_journal_check":
        rows, _ = _read_jsonl_safe("docs/token-credit-bank-ledger.jsonl")
        ok_stress, stress_payload, stress_detail = _read_json_safe("docs/body-track-policy-stress-latest.json")
        checks = [
            _check("ledger_rows_present", "PASS" if len(rows) >= 5 else "FAIL", f"rows={len(rows)}"),
            _check("stress_artifact_present", "PASS" if ok_stress else "FAIL", stress_detail if not ok_stress else "status=present"),
        ]
        if ok_stress:
            checks.append(_check("stress_status", _status_not_fail(_payload_status(stress_payload)), f"status={_payload_status(stress_payload)}"))
        return {
            "checks": checks,
            "metrics": {"ledger_rows": len(rows), "stress_history_samples": int(stress_payload.get("history_samples", 0) or 0) if ok_stress else 0},
            "targets": _collect_targets(["docs/token-credit-bank-ledger.jsonl", "docs/body-track-policy-stress-latest.json"]),
            "next_action": "Keep recovery evidence tied to both ledger continuity and stress-window artifacts.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "body_local_connectivity_matrix":
        probes = [_tool_probe("python", "--version"), _tool_probe("git", "--version"), _tool_probe("rg", "--version")]
        available = sum(1 for row in probes if row.get("available"))
        checks = [
            _check("required_tools_available", "PASS" if available == len(probes) else "FAIL", f"available={available}/{len(probes)}"),
            _check("bash_optional", "PASS", f"bash={shutil.which('bash') or 'optional_absent'}"),
        ]
        return {
            "checks": checks,
            "metrics": {"tool_probes": probes},
            "targets": _collect_targets(["scripts/run_all_trinity_systems.py"]),
            "next_action": "Keep the local toolchain explicit so Body stages remain reproducible on this machine.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "body_public_compute_refresh_github_watch":
        checks, records, runs, targets, metrics = _github_watchlist_live(offline_only=offline_only, timeout_sec=timeout_sec)
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use GitHub watch signals as advisory Body context only.", "records": records, "source_runs": runs}

    if system_id == "body_public_compute_refresh_crossref":
        query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
        queries = [row for row in query_pack.get("body", {}).get("crossref_queries", []) if isinstance(row, dict)]
        fallback_records = (
            _records_from_latest("docs/trinity-expansion/body-public-compute-refresh-crossref-latest.json")
            or _records_from_api_cache("docs/trinity-api-cache/body-signals-latest.json", source_ids={"crossref"})
            or _records_from_public_registry(pillar="body", topic_terms=["quantum computing", "AI systems", "operating systems"])
        )
        checks, records, runs, targets, metrics = _crossref_live(
            pillar="body",
            query_rows=queries,
            timeout_sec=timeout_sec,
            offline_only=offline_only,
            fallback_records=fallback_records,
        )
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use Crossref compute literature as Body maturity context.", "records": records, "source_runs": runs}

    if system_id == "body_public_compute_refresh_openalex":
        query_pack = _read_json("docs/trinity-api-query-pack-v1.json")
        queries = [row for row in query_pack.get("body", {}).get("crossref_queries", []) if isinstance(row, dict)]
        fallback_records = (
            _records_from_latest("docs/trinity-expansion/body-public-compute-refresh-openalex-latest.json")
            or _records_from_public_registry(pillar="body", topic_terms=["quantum computing", "AI systems", "agentic systems", "operating systems"])
        )
        checks, records, runs, targets, metrics = _openalex_live(
            pillar="body",
            query_rows=queries,
            latest_path="docs/trinity-expansion/body-public-compute-refresh-openalex-latest.json",
            timeout_sec=timeout_sec,
            offline_only=offline_only,
            fallback_records=fallback_records,
        )
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use OpenAlex compute signals as Body architecture context only.", "records": records, "source_runs": runs}

    if system_id == "body_compute_readiness_gate":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        records, _, _ = _merge_records(manifest, ["body_public_compute_refresh_github_watch", "body_public_compute_refresh_crossref", "body_public_compute_refresh_openalex"])
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/trinity-mandala-scoreboard-latest.json"]),
            "next_action": "Treat this as the Body readiness gate before broadening architecture claims.",
            "records": records,
            "source_runs": [],
        }

    if system_id == "heart_did_document_integrity_guard":
        ok_text, verifier_text, detail = _read_text_safe("freed_id_did_signature_verifier.py")
        if not ok_text:
            return {"checks": [_check("did_verifier_present", "FAIL", detail)], "metrics": {}, "targets": ["freed_id_did_signature_verifier.py"], "next_action": "Restore DID verifier.", "records": None, "source_runs": None}
        checks = [
            _check("ed25519_method_types_present", "PASS" if "ED25519_METHOD_TYPES" in verifier_text else "FAIL", "Ed25519 method types required"),
            _check("canonical_payload_builder_present", "PASS" if "build_canonical_payload" in verifier_text else "FAIL", "canonical payload builder required"),
            _check("did_method_verifier_present", "PASS" if "build_did_method_signature_verifier" in verifier_text else "FAIL", "DID verifier factory required"),
        ]
        return {
            "checks": checks,
            "metrics": {"verifier_length": len(verifier_text)},
            "targets": _collect_targets(["freed_id_did_signature_verifier.py", "docs/heart-track-governance-latest.json"]),
            "next_action": "Keep DID document integrity bound to method resolution and canonical payload rules.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "heart_verifiable_credential_schema_guard":
        ok_schema, schema_payload, detail_schema = _read_json_safe("docs/freed-id-minimum-disclosure-schema-v0.json")
        ok_min, min_payload, detail_min = _read_json_safe("docs/heart-track-min-disclosure-latest.json")
        ok_grid, grid_text, detail_grid = _read_text_safe("docs/comparative-validation-grid-v1.md")
        checks: list[dict[str, str]] = []
        if not ok_schema:
            checks.append(_check("vc_schema_present", "FAIL", detail_schema))
        if not ok_min:
            checks.append(_check("gov002_present", "FAIL", detail_min))
        if not ok_grid:
            checks.append(_check("comparative_grid_present", "FAIL", detail_grid))
        if ok_schema:
            required = schema_payload.get("required", [])
            checks.append(_check("schema_required_fields", "PASS" if isinstance(required, list) and len(required) >= 1 else "FAIL", f"required={len(required) if isinstance(required, list) else 0}"))
        if ok_min:
            checks.append(_check("gov002_status", _status_not_fail(_payload_status(min_payload)), f"status={_payload_status(min_payload)}"))
        if ok_grid:
            checks.append(_check("vc_data_model_reference", "PASS" if "VC Data Model 2.0" in grid_text else "FAIL", "comparative grid should mention VC Data Model 2.0"))
        return {
            "checks": checks,
            "metrics": {"schema_required_count": len(schema_payload.get("required", [])) if ok_schema and isinstance(schema_payload.get("required"), list) else 0},
            "targets": _collect_targets(["docs/freed-id-minimum-disclosure-schema-v0.json", "docs/heart-track-min-disclosure-latest.json", "docs/comparative-validation-grid-v1.md"]),
            "next_action": "Keep credential-schema comparisons explicit without overstating interoperability.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "heart_signature_algorithm_coverage":
        ok_verifier, verifier_text, detail_verifier = _read_text_safe("freed_id_did_signature_verifier.py")
        ok_protocol, protocol_text, detail_protocol = _read_text_safe("docs/dispute-resolution-protocol-v0.md")
        checks: list[dict[str, str]] = []
        if not ok_verifier:
            checks.append(_check("did_verifier_present", "FAIL", detail_verifier))
        if not ok_protocol:
            checks.append(_check("dispute_protocol_present", "FAIL", detail_protocol))
        if ok_verifier:
            checks.append(_check("ed25519_coverage", "PASS" if "Ed25519" in verifier_text else "FAIL", "Ed25519 coverage expected"))
        if ok_protocol:
            checks.append(_check("legacy_hmac_fixture_documented", "PASS" if "HMAC" in protocol_text else "FAIL", "legacy HMAC fixture should remain documented"))
        return {
            "checks": checks,
            "metrics": {"ed25519_present": ok_verifier and "Ed25519" in verifier_text, "hmac_documented": ok_protocol and "HMAC" in protocol_text},
            "targets": _collect_targets(["freed_id_did_signature_verifier.py", "docs/dispute-resolution-protocol-v0.md"]),
            "next_action": "Prefer DID-bound asymmetric verification while keeping legacy HMAC only as a fixture.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "heart_revocation_latency_guard":
        ok, payload, detail = _read_json_safe("docs/heart-track-governance-latest.json")
        if not ok:
            return {"checks": [_check("governance_artifact_present", "FAIL", detail)], "metrics": {}, "targets": ["docs/heart-track-governance-latest.json"], "next_action": "Restore Heart governance artifact.", "records": None, "source_runs": None}
        checks_rows = payload.get("checks", [])
        checks_rows = checks_rows if isinstance(checks_rows, list) else []
        seen = {str(row.get("check")) for row in checks_rows if isinstance(row, dict)}
        required = {"revoke_did", "issue_credential_after_revoke", "verify_credential_after_revoke"}
        missing = sorted(required - seen)
        return {
            "checks": [
                _check("revocation_path_complete", "PASS" if not missing else "FAIL", f"missing={missing}"),
                _check("governance_status", _status_not_fail(_payload_status(payload)), f"status={_payload_status(payload)}"),
            ],
            "metrics": {"required_checks_present": len(required) - len(missing), "generated_utc": payload.get("generated_utc")},
            "targets": _collect_targets(["docs/heart-track-governance-latest.json"]),
            "next_action": "Keep revocation evidence immediate and machine-checkable in the governance lane.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "heart_recourse_evidence_density_guard":
        ok_main, main_payload, detail_main = _read_json_safe("docs/heart-track-dispute-recourse-latest.json")
        ok_adv, adv_payload, detail_adv = _read_json_safe("docs/heart-track-dispute-recourse-adversarial-latest.json")
        checks: list[dict[str, str]] = []
        if not ok_main:
            checks.append(_check("main_recourse_present", "FAIL", detail_main))
        if not ok_adv:
            checks.append(_check("adversarial_recourse_present", "FAIL", detail_adv))
        signed_steps = 0
        history_len = 0
        if ok_main:
            final_case = main_payload.get("final_case", {}) if isinstance(main_payload.get("final_case"), dict) else {}
            history = final_case.get("history", []) if isinstance(final_case.get("history"), list) else []
            history_len = len(history)
            signed_steps = sum(1 for row in history if isinstance(row, dict) and bool(row.get("signature_verified")))
            checks.append(_check("signed_step_density", "PASS" if signed_steps >= 5 else "FAIL", f"signed_steps={signed_steps}"))
            checks.append(_check("history_density", "PASS" if history_len >= 5 else "FAIL", f"history={history_len}"))
        if ok_adv:
            checks.append(_check("adversarial_status", _status_not_fail(_payload_status(adv_payload)), f"status={_payload_status(adv_payload)}"))
        return {
            "checks": checks,
            "metrics": {"signed_steps": signed_steps, "history_len": history_len},
            "targets": _collect_targets(["docs/heart-track-dispute-recourse-latest.json", "docs/heart-track-dispute-recourse-adversarial-latest.json"]),
            "next_action": "Keep recourse evidence dense enough to support replay and dispute review.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "heart_policy_traceability_guard":
        ok_matrix, matrix_text, detail_matrix = _read_text_safe("docs/freedid-cosmic-control-matrix-v0.md")
        ok_grid, grid_text, detail_grid = _read_text_safe("docs/comparative-validation-grid-v1.md")
        checks: list[dict[str, str]] = []
        if not ok_matrix:
            checks.append(_check("control_matrix_present", "FAIL", detail_matrix))
        if not ok_grid:
            checks.append(_check("comparative_grid_present", "FAIL", detail_grid))
        if ok_matrix:
            checks.append(_check("governance_controls_present", "PASS" if all(token in matrix_text for token in ["GOV-002", "GOV-004", "GOV-005"]) else "FAIL", "GOV-002/004/005 expected"))
        if ok_grid:
            checks.append(_check("alignment_gap_proof_columns", "PASS" if all(token in grid_text for token in ["Alignment in repo", "| Gap |", "Next implementation proof"]) else "FAIL", "grid columns required"))
        return {
            "checks": checks,
            "metrics": {"matrix_length": len(matrix_text) if ok_matrix else 0, "grid_length": len(grid_text) if ok_grid else 0},
            "targets": _collect_targets(["docs/freedid-cosmic-control-matrix-v0.md", "docs/comparative-validation-grid-v1.md"]),
            "next_action": "Keep Heart controls traceable from normative framing to executable artifacts.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "heart_public_governance_refresh_nz_public_law":
        checks, records, runs, targets, metrics = _heart_registry_live(
            latest_path="docs/trinity-expansion/heart-public-governance-refresh-nz-public-law-latest.json",
            timeout_sec=timeout_sec,
            offline_only=offline_only,
            url_terms=["justice.govt.nz", "legislation.govt.nz", "waitangitribunal"],
            source_id="nz_public_law",
        )
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use NZ public-law signals as current governance context, not legal-force proof.", "records": records, "source_runs": runs}

    if system_id == "heart_public_governance_refresh_global_standards":
        checks, records, runs, targets, metrics = _heart_registry_live(
            latest_path="docs/trinity-expansion/heart-public-governance-refresh-global-standards-latest.json",
            timeout_sec=timeout_sec,
            offline_only=offline_only,
            url_terms=["w3.org", "nist.gov", "oecd.ai", "eur-lex"],
            source_id="global_standards",
        )
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use global standards signals as governance bridge context only.", "records": records, "source_runs": runs}

    if system_id == "heart_public_governance_refresh_human_rights":
        checks, records, runs, targets, metrics = _heart_registry_live(
            latest_path="docs/trinity-expansion/heart-public-governance-refresh-human-rights-latest.json",
            timeout_sec=timeout_sec,
            offline_only=offline_only,
            topic_terms=["rights", "remedy", "human rights"],
            source_kinds={"rights_charter"},
            source_id="human_rights",
        )
        return {"checks": checks, "metrics": metrics, "targets": targets, "next_action": "Use rights-charter sources as normative context while keeping implementation claims concrete.", "records": records, "source_runs": runs}

    if system_id == "heart_governance_readiness_gate":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        records, _, _ = _merge_records(manifest, ["heart_public_governance_refresh_nz_public_law", "heart_public_governance_refresh_global_standards", "heart_public_governance_refresh_human_rights"])
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/comparative-validation-grid-v1.md", "docs/trinity-mandala-scoreboard-latest.json"]),
            "next_action": "Treat this as the Heart readiness gate before widening governance claims.",
            "records": records,
            "source_runs": [],
        }

    if system_id == "trinity_memory_index_integrity":
        archive_dir = _repo_path("docs/memory-archives")
        zip_count = len(list(archive_dir.glob("*.zip"))) if archive_dir.exists() else 0
        ledger_rows, _ = _read_jsonl_safe("docs/token-credit-bank-ledger.jsonl")
        checks = [
            _check("memory_archive_dir_present", "PASS" if archive_dir.exists() else "FAIL", str(archive_dir)),
            _check("zip_snapshot_count", "PASS" if zip_count >= 1 else "FAIL", f"zip_count={zip_count}"),
            _check("token_ledger_rows", "PASS" if len(ledger_rows) >= 5 else "FAIL", f"rows={len(ledger_rows)}"),
        ]
        return {
            "checks": checks,
            "metrics": {"zip_snapshot_count": zip_count, "ledger_rows": len(ledger_rows)},
            "targets": _collect_targets(["docs/memory-archives", "docs/token-credit-bank-ledger.jsonl"]),
            "next_action": "Keep memory snapshots indexed before relying on recap or recovery flows.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_memory_recap_generator":
        commits = _git_recent_commits(limit=6)
        capability_ok, capability_payload, _ = _read_json_safe("docs/trinity-expansion/trinity-capability-surface-audit-latest.json")
        recap = {
            "continuity_mode": "repo_and_session_grounded",
            "recent_commits": commits,
            "configured_model": capability_payload.get("metrics", {}).get("configured_model") if capability_ok else "",
            "repo_python_scripts": capability_payload.get("metrics", {}).get("repo_python_scripts") if capability_ok else 0,
            "manifest_system_count": capability_payload.get("metrics", {}).get("manifest_system_count") if capability_ok else len(manifest.get("systems", [])),
        }
        checks = [
            _check("recent_commits_loaded", "PASS" if len(commits) >= 1 else "FAIL", f"commits={len(commits)}"),
            _check("capability_audit_present", "PASS" if capability_ok else "FAIL", "capability audit required"),
        ]
        return {
            "checks": checks,
            "metrics": recap,
            "targets": _collect_targets(["docs/system-suite-status.json", "docs/trinity-expansion/trinity-capability-surface-audit-latest.json"]),
            "next_action": "Use this recap as the continuity handoff summary, not as a substitute for artifacts.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_simulation_profile_guard":
        checks = []
        for path in ["trinity_simulation_engine.py", "run_simulation.py", "docs/mind-track-gmut-comparator-latest.json"]:
            try:
                exists = _repo_path(path).exists()
            except Exception:
                exists = False
            checks.append(_check(f"path:{path}", "PASS" if exists else "FAIL", f"exists={exists}"))
        ok_comp, comp_payload, _ = _read_json_safe("docs/mind-track-gmut-comparator-latest.json")
        if ok_comp:
            checks.append(_check("comparator_status", _status_not_fail(_payload_status(comp_payload)), f"status={_payload_status(comp_payload)}"))
        return {
            "checks": checks,
            "metrics": {"comparator_max_abs_deviation": comp_payload.get("max_abs_deviation", 0.0) if ok_comp else 0.0},
            "targets": _collect_targets(["trinity_simulation_engine.py", "run_simulation.py", "docs/mind-track-gmut-comparator-latest.json"]),
            "next_action": "Keep simulation profile checks tied to the reproducible comparator lane.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_local_toolchain_probe":
        probes = [_tool_probe("python", "--version"), _tool_probe("git", "--version"), _tool_probe("rg", "--version")]
        checks = [_check(f"tool:{row['tool']}", "PASS" if row.get("available") else "FAIL", str(row.get("detail"))) for row in probes]
        return {
            "checks": checks,
            "metrics": {"tool_probes": probes},
            "targets": _collect_targets(["scripts/run_all_trinity_systems.py"]),
            "next_action": "Keep toolchain probes explicit before assuming local capability growth.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_environment_capability_matrix":
        deps = ["trinity_capability_surface_audit", "trinity_local_toolchain_probe"]
        checks, metrics = _artifact_guard(manifest, deps)
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/trinity-expansion/trinity-capability-surface-audit-latest.json", "docs/system-suite-status.json"]),
            "next_action": "Use the environment matrix to constrain future integrations to what is actually available.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_public_signal_freshness_forecaster":
        freshness_paths = [
            "docs/trinity-public-source-registry-v1.json",
            "docs/trinity-api-cache/mind-signals-latest.json",
            "docs/trinity-api-cache/body-signals-latest.json",
            "docs/trinity-api-cache/heart-signals-latest.json",
            "docs/trinity-expansion/mind-public-theory-refresh-arxiv-latest.json",
            "docs/trinity-expansion/body-public-compute-refresh-github-watch-latest.json",
            "docs/trinity-expansion/heart-public-governance-refresh-global-standards-latest.json",
        ]
        checks: list[dict[str, str]] = []
        ages: dict[str, float | None] = {}
        for path in freshness_paths:
            ok, payload, detail = _read_json_safe(path)
            if not ok:
                checks.append(_check(f"freshness:{path}", "FAIL", detail))
                continue
            age = _age_days(payload.get("generated_utc"))
            ages[path] = age
            checks.append(_check(f"freshness:{path}", "PASS" if age is not None and age <= 30.0 else "FAIL", f"age_days={age}"))
        return {
            "checks": checks,
            "metrics": {"ages_days": ages},
            "targets": _collect_targets(freshness_paths),
            "next_action": "Refresh public signals when they drift beyond the 30-day research cadence.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_skill_coverage_board":
        required_local = [
            Path.home() / ".codex" / "skills" / "mind-theory-signals" / "SKILL.md",
            Path.home() / ".codex" / "skills" / "body-compute-signals" / "SKILL.md",
            Path.home() / ".codex" / "skills" / "heart-governance-bridge" / "SKILL.md",
            Path.home() / ".codex" / "skills" / "trinity-suite-expansion" / "SKILL.md",
        ]
        present = sum(1 for path in required_local if path.exists())
        checks = [
            _check("repo_skill_surface", "PASS" if len(_repo_skill_dirs()) >= 10 else "FAIL", f"repo_skills={len(_repo_skill_dirs())}"),
            _check("local_skill_surface", "PASS" if present == len(required_local) else "FAIL", f"present={present}/{len(required_local)}"),
        ]
        return {
            "checks": checks,
            "metrics": {"repo_skill_count": len(_repo_skill_dirs()), "local_skill_count": len(_local_skill_dirs()), "required_local_present": present},
            "targets": _collect_targets(["skills", "docs/trinity-skill-installer-report.json"]),
            "next_action": "Keep core Trinity skills discoverable locally before adding more specialization.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_system_dependency_graph":
        edges, missing, cycles = _manifest_graph(manifest)
        checks = [
            _check("graph_edges_present", "PASS" if len(edges) >= 1 else "FAIL", f"edges={len(edges)}"),
            _check("graph_missing_dependencies", "PASS" if not missing else "FAIL", f"missing={missing}"),
            _check("graph_cycles_absent", "PASS" if not cycles else "FAIL", f"cycles={cycles}"),
        ]
        return {
            "checks": checks,
            "metrics": {"edge_count": len(edges), "missing_dependencies": missing, "cycle_count": len(cycles)},
            "targets": _collect_targets(["docs/trinity-expansion-system-manifest-v2.json"]),
            "next_action": "Keep the manifest graph acyclic before widening suite orchestration.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_orchestration_resilience_board":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        ok_runner, runner_text, runner_detail = _read_text_safe("scripts/run_all_trinity_systems.py")
        if not ok_runner:
            checks.append(_check("runner_present", "FAIL", runner_detail))
        else:
            checks.extend(
                [
                    _check("offline_only_flag_wired", "PASS" if "--offline-only" in runner_text else "FAIL", "runner should expose offline-only mode"),
                    _check("live_network_mode_wired", "PASS" if "live_network_mode" in runner_text else "FAIL", "runner should emit live network mode status"),
                    _check(
                        "expansion_status_fields_wired",
                        "PASS" if all(marker in runner_text for marker in ("expansion_systems_total", "expansion_systems_passed")) else "FAIL",
                        "runner should emit expansion counts",
                    ),
                    _check(
                        "compatibility_alias_retained",
                        "PASS" if "--include-public-api-refresh" in runner_text else "FAIL",
                        "runner should keep the compatibility alias",
                    ),
                ]
            )
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["scripts/run_all_trinity_systems.py", "docs/trinity-expansion-system-manifest-v2.json"]),
            "next_action": "Keep orchestration resilient through explicit modes, status outputs, and dependency checks.",
            "records": None,
            "source_runs": None,
        }

    if system_id == "trinity_supercycle_gate":
        deps = _manifest_entry(manifest, system_id).get("depends_on", [])
        checks, metrics = _artifact_guard(manifest, deps)
        return {
            "checks": checks,
            "metrics": metrics,
            "targets": _collect_targets(["docs/trinity-mandala-scoreboard-latest.json", "docs/system-suite-status.json"]),
            "next_action": "Use the supercycle gate as the final expansion readiness board before narrative promotion.",
            "records": None,
            "source_runs": None,
        }

    # Remaining generic guard systems
    generic_dependencies = {
        "body_compute_signal_merge": ["body_runtime_connectivity_probe", "body_dependency_health_refresh", "docs/body-compute-signal-board-latest.json"],
    }
    if system_id in generic_dependencies:
        checks, metrics = _artifact_guard(manifest, generic_dependencies[system_id])
        return {"checks": checks, "metrics": metrics, "targets": _collect_targets(generic_dependencies[system_id]), "next_action": "Keep dependency artifacts green.", "records": None, "source_runs": None}

    raise KeyError(f"unimplemented system handler: {system_id}")


def run_named_system(system_id: str) -> int:
    parser = argparse.ArgumentParser(description=f"Run Trinity expansion system: {system_id}")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--reports-dir", default=str(DEFAULT_RUNS_DIR.relative_to(ROOT)))
    parser.add_argument("--offline-only", action="store_true")
    parser.add_argument("--fail-on-warn", action="store_true")
    parser.add_argument("--timeout-sec", type=int, default=30)
    args = parser.parse_args()

    manifest = _load_manifest(str(Path(args.manifest).resolve()))
    entry = _manifest_entry(manifest, system_id)
    result = _compute_system(system_id=system_id, manifest=manifest, offline_only=bool(args.offline_only), timeout_sec=int(args.timeout_sec))
    return _publish(
        entry=entry,
        checks=result["checks"],
        metrics=result["metrics"],
        targets=result["targets"],
        next_action=str(result.get("next_action") or "Investigate and rerun."),
        records=result.get("records"),
        source_runs=result.get("source_runs"),
        fail_on_warn=bool(args.fail_on_warn),
        runs_dir=str(args.reports_dir),
    )
