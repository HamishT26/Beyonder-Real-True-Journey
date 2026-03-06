#!/usr/bin/env python3
"""Refresh cached public Heart signals from World Bank, OECD, and data.govt.nz."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
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

OECD_NS = {
    "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}


def _world_bank_records(entry: dict[str, Any], timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    request_url = (
        f"https://api.worldbank.org/v2/country/{entry['country']}/indicator/{entry['indicator']}"
        "?format=json&per_page=5"
    )
    payload = fetch_json(request_url, timeout_sec=timeout_sec)
    rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
    chosen = next((row for row in rows if row.get("value") is not None), rows[0] if rows else {})
    record = {
        "source_id": "worldbank",
        "record_id": f"{entry['country']}-{entry['indicator']}",
        "signal_type": entry["signal_type"],
        "title": str(chosen.get("indicator", {}).get("value") or entry["indicator"]),
        "published_at": f"{chosen.get('date', '1970')}-01-01",
        "source_url": request_url,
        "summary": compact_text(
            f"World Bank governance signal for {chosen.get('country', {}).get('value', entry['country'])}: "
            f"{chosen.get('indicator', {}).get('value', entry['indicator'])}."
        ),
        "metrics": {
            "country": chosen.get("country", {}).get("value", entry["country"]),
            "indicator_id": chosen.get("indicator", {}).get("id", entry["indicator"]),
            "value": chosen.get("value"),
            "date": chosen.get("date"),
        },
        "tags": ["heart", "worldbank", entry["indicator"]],
        "repo_relevance": {
            "summary": entry["repo_relevance"],
            "targets": entry["repo_targets"],
        },
    }
    source_runs = [
        {
            "api_id": "worldbank",
            "request_id": entry["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": 1,
        }
    ]
    return [record], source_runs


def _oecd_records(entry: dict[str, Any], timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    request_url = "https://sdmx.oecd.org/public/rest/dataflow/all/all/latest"
    xml_text = fetch_text(request_url, accept="application/xml", timeout_sec=timeout_sec)
    root = ET.fromstring(xml_text)
    keyword = str(entry["keyword"]).lower()
    matches: list[dict[str, Any]] = []
    for node in root.findall(".//structure:Dataflow", OECD_NS):
        flow_id = str(node.attrib.get("id") or "")
        name = ""
        for child in node.findall("common:Name", OECD_NS):
            if child.text:
                name = child.text.strip()
                break
        haystack = f"{flow_id} {name}".lower()
        if keyword in haystack:
            matches.append({"flow_id": flow_id, "name": name or flow_id})
        if len(matches) >= int(entry.get("limit", 2)):
            break

    records = [
        {
            "source_id": "oecd",
            "record_id": row["flow_id"],
            "signal_type": entry["signal_type"],
            "title": row["name"],
            "published_at": iso_now()[:10],
            "source_url": request_url,
            "summary": compact_text(f"OECD dataflow catalog match for keyword '{entry['keyword']}'."),
            "metrics": {
                "flow_id": row["flow_id"],
                "keyword": entry["keyword"],
            },
            "tags": ["heart", "oecd", str(entry["keyword"]).lower()],
            "repo_relevance": {
                "summary": entry["repo_relevance"],
                "targets": entry["repo_targets"],
            },
        }
        for row in matches
    ]
    source_runs = [
        {
            "api_id": "oecd",
            "request_id": entry["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": len(records),
        }
    ]
    return records, source_runs


def _data_govt_records(entry: dict[str, Any], limit: int, timeout_sec: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    request_url = (
        "https://catalogue.data.govt.nz/api/3/action/package_search"
        f"?q={quote_plus(str(entry['query']))}&rows={limit}"
    )
    payload = fetch_json(request_url, timeout_sec=timeout_sec)
    results = payload.get("result", {}).get("results", []) if isinstance(payload, dict) else []
    records: list[dict[str, Any]] = []
    for item in results:
        records.append(
            {
                "source_id": "data_govt_nz",
                "record_id": str(item.get("id") or item.get("name") or entry["query_id"]),
                "signal_type": entry["signal_type"],
                "title": compact_text(str(item.get("title") or item.get("name") or "")),
                "published_at": str(item.get("metadata_modified") or item.get("modified") or "1970-01-01")[:10],
                "source_url": f"https://catalogue.data.govt.nz/dataset/{item.get('name')}",
                "summary": compact_text(str(item.get("notes") or f"data.govt.nz package search signal for {entry['query']}.")),
                "metrics": {
                    "organization": item.get("organization", {}).get("title") if isinstance(item.get("organization"), dict) else None,
                    "num_resources": len(item.get("resources", [])),
                    "query": entry["query"],
                },
                "tags": ["heart", "data.govt.nz", *entry.get("tags", [])],
                "repo_relevance": {
                    "summary": entry["repo_relevance"],
                    "targets": entry["repo_targets"],
                },
            }
        )
    source_runs = [
        {
            "api_id": "data_govt_nz",
            "request_id": entry["query_id"],
            "request_url": request_url,
            "status": "PASS",
            "record_count": len(records),
        }
    ]
    return records, source_runs


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh cached Trinity Heart public API signals.")
    parser.add_argument("--manifest", default="docs/trinity-api-source-manifest-v1.json")
    parser.add_argument("--query-pack", default="docs/trinity-api-query-pack-v1.json")
    parser.add_argument("--reports-dir", default="docs/trinity-api-cache/heart-runs")
    parser.add_argument("--latest-json", default="docs/trinity-api-cache/heart-signals-latest.json")
    parser.add_argument("--limit-per-query", type=int, default=2)
    parser.add_argument("--timeout-sec", type=int, default=30)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    query_pack = load_query_pack(args.query_pack)
    manifest_entries = manifest_entries_for_pillar(manifest, "heart")
    api_ids = sorted(str(entry["api_id"]) for entry in manifest_entries)

    records: list[dict[str, Any]] = []
    source_runs: list[dict[str, Any]] = []
    for entry in query_pack["heart"]["world_bank_indicators"]:
        rows, runs = _world_bank_records(entry, args.timeout_sec)
        records.extend(rows)
        source_runs.extend(runs)
    for entry in query_pack["heart"]["oecd_keywords"]:
        rows, runs = _oecd_records(entry, args.timeout_sec)
        records.extend(rows)
        source_runs.extend(runs)
    for entry in query_pack["heart"]["data_govt_queries"]:
        rows, runs = _data_govt_records(entry, args.limit_per_query, args.timeout_sec)
        records.extend(rows)
        source_runs.extend(runs)

    records = sort_records(records)
    payload = {
        "generated_utc": iso_now(),
        "pillar": "heart",
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
        stem="heart-signals",
    )
    print("overall_status=PASS")
    print(f"record_count={len(records)}")
    print(f"timestamped_json={timestamped_json}")
    print(f"latest_json={latest_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
