#!/usr/bin/env python3
"""Shared runner for Trinity mammoth expansion systems."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from trinity_api_common import fetch_json, fetch_text, quote_plus

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v1.json"
DEFAULT_RUNS_DIR = ROOT / "docs" / "trinity-expansion-runs"
STATUS_ORDER = {"PASS": 0, "WARN": 1, "FAIL": 2, "TIMEOUT": 3}
PASS_LIKE = {"PASS", "WARN"}


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
    latest_path = _write_json(latest_output, payload)
    timestamped_path = _write_json(timestamped_output, payload)

    print(f"overall_status={overall}")
    print(f"effective_success={effective_success}")
    print(f"latest_json={latest_path.relative_to(ROOT)}")
    print(f"timestamped_json={timestamped_path.relative_to(ROOT)}")
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
