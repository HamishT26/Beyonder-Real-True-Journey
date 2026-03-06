#!/usr/bin/env python3
"""Refresh cached public Body signals from Crossref and GitHub."""

from __future__ import annotations

import argparse
from typing import Any

from trinity_api_common import (
    aggregate_candidate_targets,
    compact_text,
    date_from_parts,
    fetch_json,
    iso_now,
    load_manifest,
    load_query_pack,
    manifest_entries_for_pillar,
    quote_plus,
    save_json_run,
    sort_records,
    strip_html,
)


def _crossref_records(query: dict[str, Any], limit: int, timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    term = str(query["query"])
    request_url = f"https://api.crossref.org/works?query.title={quote_plus(term)}&rows={limit}&sort=relevance"
    payload = fetch_json(request_url, timeout_sec=timeout_sec)
    items = payload.get("message", {}).get("items", []) if isinstance(payload, dict) else []
    records: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        title_parts = item.get("title", [])
        title = compact_text(title_parts[0] if title_parts else term, limit=160)
        published_at = date_from_parts(
            item.get("published-online", {}).get("date-parts")
            or item.get("published-print", {}).get("date-parts")
            or item.get("issued", {}).get("date-parts")
        )
        source_url = str(item.get("URL") or item.get("DOI") or "")
        records.append(
            {
                "source_id": "crossref",
                "record_id": str(item.get("DOI") or source_url or f"{query['query_id']}-crossref-{index}"),
                "signal_type": query["signal_type"],
                "title": title,
                "published_at": published_at,
                "source_url": source_url,
                "summary": strip_html(str(item.get("abstract") or "")) or compact_text(
                    f"Crossref metadata for {term} with publisher {item.get('publisher', 'unknown')}."
                ),
                "metrics": {
                    "publisher": item.get("publisher"),
                    "is_referenced_by_count": item.get("is-referenced-by-count"),
                    "query_id": query["query_id"],
                    "query": term,
                },
                "tags": ["body", "crossref", *[str(value) for value in item.get("subject", [])[:3]]],
                "repo_relevance": {
                    "summary": query["repo_relevance"],
                    "targets": query["repo_targets"],
                },
            }
        )
    source_runs = [
        {
            "api_id": "crossref",
            "request_id": query["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": len(records),
        }
    ]
    return records, source_runs


def _github_watchlist_records(entry: dict[str, Any], timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    repo = str(entry["repo"])
    request_url = f"https://api.github.com/repos/{repo}"
    payload = fetch_json(request_url, timeout_sec=timeout_sec)
    if not isinstance(payload, dict):
        raise ValueError(f"Unexpected GitHub payload for {repo}")
    record = {
        "source_id": "github",
        "record_id": str(payload.get("full_name") or repo),
        "signal_type": entry["signal_type"],
        "title": str(payload.get("full_name") or repo),
        "published_at": str(payload.get("pushed_at") or payload.get("updated_at") or "1970-01-01")[:10],
        "source_url": str(payload.get("html_url") or request_url),
        "summary": compact_text(str(payload.get("description") or f"GitHub watchlist signal for {repo}.")),
        "metrics": {
            "stargazers_count": payload.get("stargazers_count"),
            "watchers_count": payload.get("watchers_count"),
            "open_issues_count": payload.get("open_issues_count"),
            "default_branch": payload.get("default_branch"),
        },
        "tags": ["body", "github", *entry.get("tags", [])],
        "repo_relevance": {
            "summary": entry["repo_relevance"],
            "targets": entry["repo_targets"],
        },
    }
    source_runs = [
        {
            "api_id": "github",
            "request_id": entry["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": 1,
        }
    ]
    return [record], source_runs


def _github_search_records(query: dict[str, Any], limit: int, timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    term = str(query["query"])
    request_url = (
        "https://api.github.com/search/repositories"
        f"?q={quote_plus(term)}&per_page={limit}&sort=updated&order=desc"
    )
    payload = fetch_json(request_url, timeout_sec=timeout_sec)
    items = payload.get("items", []) if isinstance(payload, dict) else []
    records: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        records.append(
            {
                "source_id": "github",
                "record_id": str(item.get("full_name") or f"{query['query_id']}-github-search-{index}"),
                "signal_type": query["signal_type"],
                "title": str(item.get("full_name") or term),
                "published_at": str(item.get("updated_at") or "1970-01-01")[:10],
                "source_url": str(item.get("html_url") or request_url),
                "summary": compact_text(str(item.get("description") or f"GitHub search signal for {term}.")),
                "metrics": {
                    "stargazers_count": item.get("stargazers_count"),
                    "watchers_count": item.get("watchers_count"),
                    "open_issues_count": item.get("open_issues_count"),
                    "query_id": query["query_id"],
                    "query": term,
                },
                "tags": ["body", "github", "search"],
                "repo_relevance": {
                    "summary": query["repo_relevance"],
                    "targets": query["repo_targets"],
                },
            }
        )
    source_runs = [
        {
            "api_id": "github",
            "request_id": query["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": len(records),
        }
    ]
    return records, source_runs


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh cached Trinity Body public API signals.")
    parser.add_argument("--manifest", default="docs/trinity-api-source-manifest-v1.json")
    parser.add_argument("--query-pack", default="docs/trinity-api-query-pack-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-api-cache/body-runs")
    parser.add_argument("--latest-json", default="docs/trinity-api-cache/body-signals-latest.json")
    parser.add_argument("--limit-per-query", type=int, default=2)
    parser.add_argument("--timeout-sec", type=int, default=30)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    query_pack = load_query_pack(args.query_pack)
    manifest_entries = manifest_entries_for_pillar(manifest, "body")
    api_ids = sorted(str(entry["api_id"]) for entry in manifest_entries)

    records: list[dict[str, Any]] = []
    source_runs: list[dict[str, Any]] = []
    for query in query_pack["body"]["crossref_queries"]:
        rows, runs = _crossref_records(query, args.limit_per_query, args.timeout_sec)
        records.extend(rows)
        source_runs.extend(runs)
    for entry in query_pack["body"]["github_watchlist"]:
        rows, runs = _github_watchlist_records(entry, args.timeout_sec)
        records.extend(rows)
        source_runs.extend(runs)
    for query in query_pack["body"]["github_search_queries"]:
        rows, runs = _github_search_records(query, 1, args.timeout_sec)
        records.extend(rows)
        source_runs.extend(runs)

    records = sort_records(records)
    payload = {
        "generated_utc": iso_now(),
        "pillar": "body",
        "refresh_window_days": int(manifest.get("refresh_window_days", 30)),
        "apis_checked": api_ids,
        "source_runs": source_runs,
        "records": records,
        "candidate_repo_targets": aggregate_candidate_targets(records),
    }
    timestamped_json, latest_json = save_json_run(
        payload=payload,
        latest_json=args.latest_json,
        reports_dir=args.reports_dir,
        stem="body-signals",
    )
    print("overall_status=PASS")
    print(f"record_count={len(records)}")
    print(f"timestamped_json={timestamped_json}")
    print(f"latest_json={latest_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
