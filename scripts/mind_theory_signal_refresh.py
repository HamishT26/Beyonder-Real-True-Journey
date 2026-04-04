#!/usr/bin/env python3
"""Refresh cached public Mind signals from arXiv and OpenAlex."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from trinity_api_common import (
    aggregate_candidate_targets,
    compact_text,
    fetch_json,
    fetch_text,
    iso_now,
    load_manifest,
    load_query_pack,
    manifest_entries_for_pillar,
    quote_plus,
    save_json_run,
    sort_records,
)

ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _load_cached_payload(path_str: str) -> dict[str, Any] | None:
    path = Path(path_str)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _cache_fallback_payload(existing: dict[str, Any], reason: Exception, latest_json: str) -> dict[str, Any]:
    cached_records = existing.get("records", [])
    cached_runs = existing.get("source_runs", [])
    payload = dict(existing)
    payload["generated_utc"] = iso_now()
    payload["overall_status"] = "PASS"
    payload["effective_success"] = True
    payload["refresh_mode"] = "cache_fallback"
    payload["fallback_reason"] = compact_text(str(reason), limit=240)
    if not isinstance(cached_records, list):
        cached_records = []
    normalized_runs: list[dict[str, Any]] = []
    if isinstance(cached_runs, list):
        for index, row in enumerate(cached_runs, start=1):
            if isinstance(row, dict):
                normalized = dict(row)
                normalized.setdefault("request_url", latest_json)
                normalized.setdefault("request_id", f"cached-source-run-{index}")
                normalized_runs.append(normalized)
    payload["record_count"] = len(cached_records)
    payload["records"] = cached_records
    payload["source_runs"] = [
        *normalized_runs,
        {
            "api_id": "cache_fallback",
            "request_id": "mind_theory_signal_refresh",
            "request_url": latest_json,
            "status": "PASS",
            "record_count": len(cached_records),
            "detail": compact_text(f"reused cached latest because live refresh failed: {reason}", limit=240),
        },
    ]
    payload["candidate_repo_targets"] = aggregate_candidate_targets(cached_records)
    return payload


def _arxiv_records(query: dict[str, Any], limit: int, timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    term = str(query["query"])
    request_url = (
        "https://export.arxiv.org/api/query"
        f"?search_query={quote_plus(f'all:\"{term}\"')}&start=0&max_results={limit}"
        "&sortBy=submittedDate&sortOrder=descending"
    )
    xml_text = fetch_text(request_url, accept="application/atom+xml", timeout_sec=timeout_sec)
    root = ET.fromstring(xml_text)
    entries = root.findall("atom:entry", ARXIV_NS)
    records: list[dict[str, Any]] = []
    for index, entry in enumerate(entries, start=1):
        entry_id = entry.findtext("atom:id", default="", namespaces=ARXIV_NS)
        title = compact_text(entry.findtext("atom:title", default="", namespaces=ARXIV_NS), limit=160)
        published_at = entry.findtext("atom:published", default="", namespaces=ARXIV_NS)[:10]
        summary = compact_text(entry.findtext("atom:summary", default="", namespaces=ARXIV_NS))
        categories = sorted({node.attrib.get("term", "") for node in entry.findall("atom:category", ARXIV_NS) if node.attrib.get("term")})
        records.append(
            {
                "source_id": "arxiv",
                "record_id": entry_id or f"{query['query_id']}-arxiv-{index}",
                "signal_type": query["signal_type"],
                "title": title,
                "published_at": published_at or "1970-01-01",
                "source_url": entry_id,
                "summary": summary,
                "metrics": {
                    "authors": len(entry.findall("atom:author", ARXIV_NS)),
                    "categories": categories,
                    "query_id": query["query_id"],
                    "query": term,
                },
                "tags": ["mind", "theory", *categories[:5]],
                "repo_relevance": {
                    "summary": query["repo_relevance"],
                    "targets": query["repo_targets"],
                },
            }
        )
    source_runs = [
        {
            "api_id": "arxiv",
            "request_id": query["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": len(records),
        }
    ]
    return records, source_runs


def _openalex_records(query: dict[str, Any], limit: int, timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    term = str(query["query"])
    request_url = (
        "https://api.openalex.org/works"
        f"?search={quote_plus(term)}&per-page={limit}&sort=relevance_score:desc"
    )
    payload = fetch_json(request_url, timeout_sec=timeout_sec)
    results = payload.get("results", []) if isinstance(payload, dict) else []
    records: list[dict[str, Any]] = []
    for index, item in enumerate(results, start=1):
        title = compact_text(str(item.get("display_name") or item.get("title") or ""), limit=160)
        source_url = str(item.get("id") or item.get("doi") or "")
        records.append(
            {
                "source_id": "openalex",
                "record_id": source_url or f"{query['query_id']}-openalex-{index}",
                "signal_type": query["signal_type"],
                "title": title,
                "published_at": str(item.get("publication_date") or f"{item.get('publication_year', 1970)}-01-01")[:10],
                "source_url": source_url,
                "summary": compact_text(
                    f"OpenAlex relevance score {item.get('relevance_score', 0)} with cited_by_count {item.get('cited_by_count', 0)}."
                ),
                "metrics": {
                    "relevance_score": item.get("relevance_score"),
                    "cited_by_count": item.get("cited_by_count"),
                    "query_id": query["query_id"],
                    "query": term,
                },
                "tags": ["mind", "theory", "openalex"],
                "repo_relevance": {
                    "summary": query["repo_relevance"],
                    "targets": query["repo_targets"],
                },
            }
        )
    source_runs = [
        {
            "api_id": "openalex",
            "request_id": query["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": len(records),
        }
    ]
    return records, source_runs


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh cached Trinity Mind public API signals.")
    parser.add_argument("--manifest", default="docs/trinity-api-source-manifest-v1.json")
    parser.add_argument("--query-pack", default="docs/trinity-api-query-pack-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-api-cache/mind-runs")
    parser.add_argument("--latest-json", default="docs/trinity-api-cache/mind-signals-latest.json")
    parser.add_argument("--limit-per-query", type=int, default=2)
    parser.add_argument("--timeout-sec", type=int, default=30)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    query_pack = load_query_pack(args.query_pack)
    manifest_entries = manifest_entries_for_pillar(manifest, "mind")
    api_ids = sorted(str(entry["api_id"]) for entry in manifest_entries)
    queries = query_pack["mind"]["queries"]

    try:
        records: list[dict[str, Any]] = []
        source_runs: list[dict[str, Any]] = []
        for query in queries:
            if "arxiv" in query["api_ids"]:
                rows, runs = _arxiv_records(query, args.limit_per_query, args.timeout_sec)
                records.extend(rows)
                source_runs.extend(runs)
            if "openalex" in query["api_ids"]:
                rows, runs = _openalex_records(query, args.limit_per_query, args.timeout_sec)
                records.extend(rows)
                source_runs.extend(runs)

        records = sort_records(records)
        payload = {
            "generated_utc": iso_now(),
            "pillar": "mind",
            "overall_status": "PASS",
            "effective_success": True,
            "refresh_mode": "live_refresh",
            "record_count": len(records),
            "refresh_window_days": int(manifest.get("refresh_window_days", 30)),
            "apis_checked": api_ids,
            "source_runs": source_runs,
            "records": records,
            "candidate_repo_targets": aggregate_candidate_targets(records),
        }
    except Exception as exc:  # noqa: BLE001
        existing = _load_cached_payload(args.latest_json)
        if existing is None:
            raise
        payload = _cache_fallback_payload(existing, exc, args.latest_json)
    timestamped_json, latest_json = save_json_run(
        payload=payload,
        latest_json=args.latest_json,
        reports_dir=args.reports_dir,
        stem="mind-signals",
    )
    print("overall_status=PASS")
    print(f"record_count={int(payload.get('record_count', 0) or 0)}")
    if payload.get("refresh_mode") == "cache_fallback":
        print("refresh_mode=cache_fallback")
    print(f"timestamped_json={timestamped_json}")
    print(f"latest_json={latest_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
