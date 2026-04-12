#!/usr/bin/env python3
"""Run the V38 maximal practical project-scoped enterprise API sweep."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import PROJECT_ID, google_request
from trinity_v36_cloud_common import ensure_service_enabled, load_primary_service_account, now_iso, write_json, write_text
from trinity_v38_journey_digest import DEFAULT_SOURCE, extract_api_titles
from trinity_v38_windows_operator_probe import build_gcloud_env, ensure_operator_lane

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-enterprise-api-sweep-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-enterprise-api-sweep-v1.md"
DEFAULT_DIGEST = ROOT / "docs" / "auto-generated" / "v38-journey-advisory-digest-v1.json"
SEEDED_SERVICE_NAMES = {
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
    "bigtable.googleapis.com",
    "bigtableadmin.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "gkeconnect.googleapis.com",
    "gkehub.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "oslogin.googleapis.com",
    "secretmanager.googleapis.com",
    "servicemanagement.googleapis.com",
    "serviceusage.googleapis.com",
}
TITLE_SERVICE_OVERRIDES = {
    "Anthos GKE API": "gkehub.googleapis.com",
    "Cloud Bigtable Admin API": "bigtableadmin.googleapis.com",
    "Cloud Bigtable API": "bigtable.googleapis.com",
    "Cloud Bigtable Table Admin API": "bigtableadmin.googleapis.com",
    "Cloud OS Login API": "oslogin.googleapis.com",
    "Cloud Resource Manager API": "cloudresourcemanager.googleapis.com",
    "Cloud Run Admin API": "run.googleapis.com",
    "IAM Service Account Credentials API": "iamcredentials.googleapis.com",
    "Identity and Access Management (IAM) API": "iam.googleapis.com",
    "Kubernetes Engine API": "container.googleapis.com",
    "Service Management API": "servicemanagement.googleapis.com",
    "Service Usage API": "serviceusage.googleapis.com",
    "Vertex AI API": "aiplatform.googleapis.com",
}
CONSUMER_SKIP_MARKERS = (
    "admin sdk",
    "aerial view",
    "air quality",
    "calendar",
    "custom search",
    "directions",
    "distance matrix",
    "gmail",
    "google analytics",
    "google docs",
    "google drive",
    "google play",
    "google sheets",
    "google slides",
    "google vault",
    "google wallet",
    "geocoding",
    "maps ",
    "page speed",
    "pagespeed",
    "places ",
    "pollen",
    "roads",
    "route",
    "solar",
    "street view",
    "time zone",
    "weather",
)
ORG_OR_ONBOARDING_SKIP_MARKERS = (
    "apigee",
    "chronicle",
    "cloud identity",
    "earth engine",
    "organization policy",
    "subscribe with google",
)


def normalize(value: str) -> str:
    lowered = re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()
    lowered = re.sub(r"\bapi\b", "", lowered).strip()
    return re.sub(r"\s+", " ", lowered)


def service_inventory(project_id: str, token: str) -> dict[str, Any]:
    enabled: list[str] = []
    page_token = ""
    enabled_pages: list[dict[str, Any]] = []
    while True:
        suffix = f"&pageToken={page_token}" if page_token else ""
        response = google_request(
            "GET",
            f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services?pageSize=200&filter=state:ENABLED{suffix}",
            token,
            timeout=240,
        )
        enabled_pages.append({"status": response["status"], "body_excerpt": response.get("body_text", "")[:1200]})
        if response["status"] != 200:
            return {"enabled_status": response["status"], "enabled": [], "available": [], "raw_pages": {"enabled": enabled_pages}}
        parsed = response.get("parsed", {})
        for row in parsed.get("services", []) if isinstance(parsed, dict) else []:
            if not isinstance(row, dict):
                continue
            config = row.get("config", {}) if isinstance(row.get("config"), dict) else {}
            name = str(config.get("name") or row.get("name") or "")
            if name:
                enabled.append(name)
        page_token = str(parsed.get("nextPageToken") or "") if isinstance(parsed, dict) else ""
        if not page_token:
            break

    available = available_catalog_via_gcloud(project_id)
    available_pages: list[dict[str, Any]] = []
    available_status = 200
    if not available:
        page_token = ""
        while True:
            suffix = f"&pageToken={page_token}" if page_token else ""
            response = google_request(
                "GET",
                f"https://servicemanagement.googleapis.com/v1/services?pageSize=200{suffix}",
                token,
                timeout=240,
            )
            available_pages.append({"status": response["status"], "body_excerpt": response.get("body_text", "")[:1200]})
            if response["status"] != 200:
                available_status = response["status"]
                available = []
                break
            parsed = response.get("parsed", {})
            for row in parsed.get("services", []) if isinstance(parsed, dict) else []:
                if not isinstance(row, dict):
                    continue
                name = str(row.get("serviceName") or row.get("name") or "")
                title = str(row.get("title") or "")
                if name.endswith(".googleapis.com"):
                    available.append({"name": name, "title": title})
            page_token = str(parsed.get("nextPageToken") or "") if isinstance(parsed, dict) else ""
            if not page_token:
                break

    return {
        "enabled_status": 200,
        "available_status": available_status,
        "enabled": sorted(set(enabled)),
        "available": available,
        "raw_pages": {"enabled": enabled_pages, "available": available_pages},
    }


def available_catalog_via_gcloud(project_id: str) -> list[dict[str, str]]:
    operator = ensure_operator_lane(str(Path.home() / "GCP service account keys.txt"), bootstrap=True)
    gcloud_path = str(operator.get("gcloud_path") or "")
    if operator.get("overall_status") != "PASS" or not gcloud_path:
        return []
    env = build_gcloud_env()
    proc = subprocess.run(
        [
            gcloud_path,
            "services",
            "list",
            "--available",
            "--format=json",
            "--project",
            project_id,
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if proc.returncode != 0:
        return []
    try:
        parsed = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return []
    rows: list[dict[str, str]] = []
    for item in parsed if isinstance(parsed, list) else []:
        if not isinstance(item, dict):
            continue
        config = item.get("config", {}) if isinstance(item.get("config"), dict) else {}
        name = str(config.get("name") or "")
        title = str(config.get("title") or "")
        if name.endswith(".googleapis.com"):
            rows.append({"name": name, "title": title})
    return rows


def load_api_titles(source: Path, digest_path: Path) -> list[str]:
    if digest_path.exists():
        payload = json.loads(digest_path.read_text(encoding="utf-8-sig"))
        rows = payload.get("parsed_api_titles", [])
        if isinstance(rows, list):
            titles = [str(row or "").strip() for row in rows if str(row or "").strip()]
            if titles:
                return titles
    raw_text = source.read_text(encoding="utf-8", errors="replace") if source.exists() else ""
    return extract_api_titles(raw_text)


def build_catalog_maps(available: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    by_name = {str(row.get("name") or ""): row for row in available}
    by_title: dict[str, dict[str, str]] = {}
    for row in available:
        title_key = normalize(str(row.get("title") or ""))
        if title_key and title_key not in by_title:
            by_title[title_key] = row
    return by_name, by_title


def skip_reason(title: str, service_name: str) -> str:
    haystack = f"{title} {service_name}".lower()
    if any(marker in haystack for marker in CONSUMER_SKIP_MARKERS):
        return "consumer_or_workspace_surface"
    if any(marker in haystack for marker in ORG_OR_ONBOARDING_SKIP_MARKERS):
        return "org_domain_or_external_onboarding_surface"
    return ""


def resolve_targets(api_titles: list[str], available: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    by_name, by_title = build_catalog_maps(available)
    matched: dict[str, dict[str, str]] = {}
    unmatched: list[dict[str, str]] = []

    for title in api_titles:
        service_name = TITLE_SERVICE_OVERRIDES.get(title, "")
        row = by_name.get(service_name) if service_name else None
        if row is None:
            row = by_title.get(normalize(title))
        if row is None:
            unmatched.append({"title": title, "reason": "catalog_match_missing"})
            continue
        matched[str(row["name"])] = {"title": title, "name": str(row["name"]), "catalog_title": str(row.get("title") or "")}

    for name in SEEDED_SERVICE_NAMES:
        if name in matched:
            continue
        row = by_name.get(name)
        if row:
            matched[name] = {"title": str(row.get("title") or name), "name": name, "catalog_title": str(row.get("title") or "")}
        else:
            unmatched.append({"title": name, "reason": "seeded_service_missing_from_catalog"})

    return [matched[key] for key in sorted(matched)], unmatched


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V38 Enterprise API Sweep",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Sweep state: `{payload['enterprise_api_sweep_state']}`",
        f"- Parsed V39 API titles: `{payload['requested_api_title_count']}`",
        f"- Matched services: `{payload['matched_service_count']}`",
        f"- Enabled now: `{len(payload['enabled'])}`",
        f"- Already enabled: `{len(payload['already_enabled'])}`",
        f"- Skipped: `{len(payload['skipped'])}`",
        f"- Failed: `{len(payload['failed'])}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    if payload.get("failed"):
        lines.extend(["", "## Failed", ""])
        lines.extend(
            f"- `{row['name']}`: {row.get('error_message') or row.get('reason') or 'failed'}"
            for row in payload["failed"]
        )
    if payload.get("skipped"):
        lines.extend(["", "## Skipped", ""])
        lines.extend(f"- `{row['name']}`: {row['reason']}" for row in payload["skipped"][:40])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V38 maximal practical project-scoped enterprise API sweep.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--digest-json", default=str(DEFAULT_DIGEST))
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "project_id": args.project_id,
        "overall_status": "WARN",
        "enterprise_api_sweep_state": "pending",
        "completed_steps": [],
        "blockers": [],
        "enabled": [],
        "already_enabled": [],
        "skipped": [],
        "failed": [],
    }

    api_titles = load_api_titles(Path(args.source), Path(args.digest_json))
    payload["requested_api_title_count"] = len(api_titles)
    payload["requested_api_titles"] = api_titles

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["enterprise_api_sweep_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_json(output_json, payload)
        write_text(output_md, markdown(payload))
        return 1

    token = minted["token"]
    payload["primary_identity"] = str(primary["client_email"])
    payload["service_account_path"] = str(primary["runtime_path"])
    payload["completed_steps"].append("mint_primary_token")

    inventory = service_inventory(args.project_id, token)
    payload["service_inventory"] = {
        "enabled_status": inventory.get("enabled_status"),
        "available_status": inventory.get("available_status"),
        "enabled_count": len(inventory.get("enabled", [])),
        "available_count": len(inventory.get("available", [])),
    }
    if inventory.get("enabled_status") != 200 or inventory.get("available_status") != 200:
        payload["overall_status"] = "FAIL"
        payload["enterprise_api_sweep_state"] = "blocked_service_inventory"
        payload["blockers"].append("Service Usage or Service Management inventory failed during the V38 API sweep.")
        write_json(output_json, payload)
        write_text(output_md, markdown(payload))
        return 1
    payload["completed_steps"].append("service_catalog_loaded")

    matched, unmatched = resolve_targets(api_titles, inventory["available"])
    payload["matched_service_count"] = len(matched)
    payload["matched_services"] = matched
    payload["unmatched_titles"] = unmatched
    enabled_set = set(inventory["enabled"])

    for row in matched:
        name = str(row["name"])
        title = str(row["title"])
        reason = skip_reason(title, name)
        if reason:
            payload["skipped"].append({"name": name, "title": title, "reason": reason})
            continue
        if name in enabled_set:
            payload["already_enabled"].append({"name": name, "title": title, "catalog_title": row.get("catalog_title", "")})
            continue
        result = ensure_service_enabled(args.project_id, token, name)
        error_message = str(result.get("raw_enable_response", {}).get("error", {}).get("message") or "")
        if result["final_status"] == 200 and result["final_state"] == "ENABLED":
            payload["enabled"].append(
                {
                    "name": name,
                    "title": title,
                    "catalog_title": row.get("catalog_title", ""),
                    "initial_state": result["initial_state"],
                    "enable_attempted": result["enable_attempted"],
                }
            )
            continue
        payload["failed"].append(
            {
                "name": name,
                "title": title,
                "catalog_title": row.get("catalog_title", ""),
                "initial_state": result["initial_state"],
                "final_state": result["final_state"],
                "http_status": result["final_status"],
                "error_message": error_message,
            }
        )

    payload["completed_steps"].append("maximal_practical_enablement_attempted")
    payload["anthos_seed_results"] = {
        "enabled_or_existing": [
            row["name"]
            for row in payload["enabled"] + payload["already_enabled"]
            if any(marker in row["name"] for marker in ("anthos", "gke", "container", "oslogin"))
        ],
        "failed": [
            row["name"]
            for row in payload["failed"]
            if any(marker in row["name"] for marker in ("anthos", "gke", "container", "oslogin"))
        ],
    }

    if payload["failed"]:
        payload["overall_status"] = "WARN"
        payload["enterprise_api_sweep_state"] = "maximal_practical_enablement_bounded"
    else:
        payload["overall_status"] = "PASS"
        payload["enterprise_api_sweep_state"] = "maximal_practical_enablement_applied"

    write_json(output_json, payload)
    write_text(output_md, markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
