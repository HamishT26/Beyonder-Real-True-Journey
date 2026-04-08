#!/usr/bin/env python3
"""Shared helpers for the V36 Omega split-location cloud proof lanes."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import (
    DEFAULT_GCP_KEY_BUNDLE,
    PRIMARY_REGION as LEGACY_PRIMARY_REGION,
    PROJECT_ID,
    google_request,
    load_gcp_service_accounts,
    mask_email,
    mint_access_token,
    now_iso,
    run_cmd,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v36_omega"
VERTEX_SERVICE_NAME = "aiplatform.googleapis.com"
DEFAULT_REGIONAL_LOCATION = "us-central1"
DEFAULT_MODEL_LOCATION = "global"
FLASH_FALLBACK_MODEL = "gemini-2.5-flash"
DOCUMENTED_VERTEX_PRO_CANDIDATES = [
    "gemini-3.1-pro-preview",
    "gemini-2.5-pro",
]
DOCUMENTED_CLI_ROUTE_CANDIDATES = [
    "pro",
    "gemini-3.1-pro-preview",
    "gemini-2.5-pro",
    FLASH_FALLBACK_MODEL,
]
LOCAL_RUNTIME = ROOT / ".local-runtime"
LOCAL_SITE_PACKAGES = LOCAL_RUNTIME / "site-packages"
SERVICE_ACCOUNT_RUNTIME_DIR = LOCAL_RUNTIME / "gcp-service-accounts"
PRIMARY_STAGING_BUCKET = f"gs://beyonder-v36-us-central1-staging-{PROJECT_ID}"
REASONING_ENGINE_PATTERN = re.compile(
    r"projects/\d+/locations/[a-z0-9-]+/reasoningEngines/\d+(?:/operations/\d+)?"
)


def location_host(location: str) -> str:
    normalized = str(location or "").strip()
    if normalized == "global":
        return "https://aiplatform.googleapis.com"
    return f"https://{normalized}-aiplatform.googleapis.com"


def service_url(project_id: str, service_name: str) -> str:
    return f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services/{service_name}"


def storage_bucket_url(bucket_name: str) -> str:
    return f"https://storage.googleapis.com/storage/v1/b/{bucket_name}"


def bucket_name_from_uri(bucket_uri: str) -> str:
    text = str(bucket_uri or "").strip()
    return text.replace("gs://", "", 1).split("/", 1)[0]


def ensure_service_enabled(project_id: str, token: str, service_name: str) -> dict[str, Any]:
    initial = google_request("GET", service_url(project_id, service_name), token, timeout=60)
    initial_state = str(initial.get("parsed", {}).get("state", "UNKNOWN"))
    enable_attempted = False
    enable_response: dict[str, Any] | None = None
    final = initial
    if initial_state != "ENABLED":
        enable_attempted = True
        enable_response = google_request(
            "POST",
            f"{service_url(project_id, service_name)}:enable",
            token,
            body={},
            timeout=120,
        )
        final = google_request("GET", service_url(project_id, service_name), token, timeout=60)
    return {
        "service_name": service_name,
        "initial_status": initial["status"],
        "initial_state": initial_state,
        "enable_attempted": enable_attempted,
        "enable_status": None if enable_response is None else enable_response["status"],
        "final_status": final["status"],
        "final_state": str(final.get("parsed", {}).get("state", "UNKNOWN")),
        "raw_enable_response": {} if enable_response is None else enable_response.get("parsed", {}),
    }


def ensure_staging_bucket(
    project_id: str,
    token: str,
    bucket_uri: str,
    location: str = "US-CENTRAL1",
) -> dict[str, Any]:
    bucket_name = bucket_name_from_uri(bucket_uri)
    lookup = google_request("GET", storage_bucket_url(bucket_name), token, timeout=60)
    if lookup["status"] == 200:
        parsed = lookup.get("parsed", {})
        return {
            "bucket_uri": bucket_uri,
            "bucket_name": bucket_name,
            "lookup_status": lookup["status"],
            "created": False,
            "final_status": 200,
            "location": str(parsed.get("location") or ""),
            "storage_class": str(parsed.get("storageClass") or ""),
        }

    create = google_request(
        "POST",
        f"https://storage.googleapis.com/storage/v1/b?project={project_id}",
        token,
        body={
            "name": bucket_name,
            "location": location,
            "storageClass": "STANDARD",
            "iamConfiguration": {"uniformBucketLevelAccess": {"enabled": True}},
        },
        timeout=120,
    )
    final = google_request("GET", storage_bucket_url(bucket_name), token, timeout=60)
    parsed = final.get("parsed", {}) if isinstance(final.get("parsed", {}), dict) else {}
    return {
        "bucket_uri": bucket_uri,
        "bucket_name": bucket_name,
        "lookup_status": lookup["status"],
        "create_status": create["status"],
        "created": create["status"] in {200, 201},
        "final_status": final["status"],
        "location": str(parsed.get("location") or ""),
        "storage_class": str(parsed.get("storageClass") or ""),
        "create_error": best_effort_error_message(create.get("parsed", {}), create.get("body_text", ""))[:500],
    }


def _record_from_info(alias: str, info: dict[str, Any], runtime_path: Path) -> dict[str, Any]:
    return {
        "alias": alias,
        "client_email": str(info["client_email"]),
        "project_id": str(info.get("project_id") or PROJECT_ID),
        "private_key_id": str(info.get("private_key_id", "")),
        "runtime_path": runtime_path,
        "info": info,
    }


def load_service_account_records(bundle_path: Path | str = DEFAULT_GCP_KEY_BUNDLE) -> dict[str, dict[str, Any]]:
    runtime_dir = SERVICE_ACCOUNT_RUNTIME_DIR
    runtime_dir.mkdir(parents=True, exist_ok=True)
    records: dict[str, dict[str, Any]] = {}

    bundle = load_gcp_service_accounts(Path(bundle_path))
    for row in bundle.get("records", []):
        if not isinstance(row, dict):
            continue
        alias = str(row.get("alias") or "").strip()
        if alias:
            records[alias] = row

    for alias in ("compute_default", "app_engine_default", "beyonder_real_journey_1"):
        runtime_path = runtime_dir / f"{alias}.json"
        if alias in records or not runtime_path.exists():
            continue
        info = json.loads(runtime_path.read_text(encoding="utf-8"))
        if info.get("type") != "service_account" or not info.get("client_email"):
            continue
        records[alias] = _record_from_info(alias, info, runtime_path)

    return records


def load_primary_service_account(
    bundle_path: Path | str = DEFAULT_GCP_KEY_BUNDLE,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    records = load_service_account_records(bundle_path)
    primary = (
        records.get("compute_default")
        or records.get("app_engine_default")
        or next(iter(records.values()), None)
    )
    if primary is None:
        raise RuntimeError("No primary GCP service account was available for the V36 proof lane.")
    minted = mint_access_token(primary["info"])
    return records, primary, minted


def load_compute_service_account(
    bundle_path: Path | str = DEFAULT_GCP_KEY_BUNDLE,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    records = load_service_account_records(bundle_path)
    primary = records.get("compute_default") or records.get("app_engine_default")
    if primary is None:
        raise RuntimeError("No compute-default style service account was available for the V36 proof lane.")
    minted = mint_access_token(primary["info"])
    return records, primary, minted


def generate_content_url(project_id: str, model_location: str, model_name: str) -> str:
    host = location_host(model_location)
    return (
        f"{host}/v1/projects/{project_id}/locations/{model_location}/"
        f"publishers/google/models/{model_name}:generateContent"
    )


def list_models_url(project_id: str, model_location: str) -> str:
    host = location_host(model_location)
    return (
        f"{host}/v1/projects/{project_id}/locations/{model_location}/"
        "publishers/google/models?pageSize=100"
    )


def reasoning_engines_url(project_id: str, regional_location: str) -> str:
    host = location_host(regional_location)
    return (
        f"{host}/v1beta1/projects/{project_id}/locations/{regional_location}/"
        "reasoningEngines?pageSize=20"
    )


def reasoning_engine_url(regional_location: str, resource_name: str) -> str:
    host = location_host(regional_location)
    return f"{host}/v1beta1/{resource_name}"


def memories_url(regional_location: str, engine_name: str) -> str:
    host = location_host(regional_location)
    return f"{host}/v1beta1/{engine_name}/memories?pageSize=20"


def response_text(parsed: dict[str, Any]) -> str:
    candidates = parsed.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        return ""
    first = candidates[0]
    content = first.get("content", {})
    parts = content.get("parts", [])
    if not isinstance(parts, list):
        return ""
    texts = [str(part.get("text", "")) for part in parts if isinstance(part, dict) and part.get("text")]
    return "\n".join(texts).strip()


def normalize_model_name(value: str) -> str:
    text = str(value or "").strip()
    if "/models/" in text:
        text = text.rsplit("/models/", 1)[1]
    return text


def collect_model_names(payload: Any) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()

    def add(candidate: str) -> None:
        normalized = normalize_model_name(candidate)
        if normalized and normalized not in seen:
            seen.add(normalized)
            names.append(normalized)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(item, str) and (
                    key in {"name", "displayName", "model", "modelName", "id"}
                    or "/models/" in item
                    or item.startswith("gemini-")
                    or item == "pro"
                ):
                    add(item)
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str):
            if "/models/" in value or value.startswith("gemini-") or value == "pro":
                add(value)

    walk(payload)
    return names


def prioritized_vertex_models(
    available_models: list[str],
    fallback_model: str = FLASH_FALLBACK_MODEL,
    documented_candidates: list[str] | None = None,
) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    candidate_order = documented_candidates or DOCUMENTED_VERTEX_PRO_CANDIDATES

    for model in candidate_order:
        normalized = normalize_model_name(model)
        if normalized and normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)

    for model in available_models:
        normalized = normalize_model_name(model)
        if normalized.startswith("gemini-") and normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)

    if fallback_model not in seen:
        ordered.append(fallback_model)
    return ordered


def primary_identity_fields(primary: dict[str, Any], minted: dict[str, Any]) -> dict[str, Any]:
    return {
        "primary_identity": mask_email(primary["client_email"]),
        "token_expiry_utc": minted.get("expiry_utc", ""),
        "token_scopes": minted.get("scopes", []),
    }


def build_vertex_env(
    service_account_record: dict[str, Any],
    project_id: str,
    *,
    regional_location: str = DEFAULT_REGIONAL_LOCATION,
    model_location: str = DEFAULT_MODEL_LOCATION,
    google_cloud_location: str | None = None,
) -> dict[str, str]:
    env = dict(os.environ)
    env["GOOGLE_APPLICATION_CREDENTIALS"] = str(service_account_record["runtime_path"])
    env["GOOGLE_CLOUD_PROJECT"] = project_id
    env["GOOGLE_CLOUD_LOCATION"] = google_cloud_location or model_location or regional_location
    env["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    env["TRINITY_V36_REGIONAL_LOCATION"] = regional_location
    env["TRINITY_V36_MODEL_LOCATION"] = model_location
    env.pop("GOOGLE_GENAI_USE_GCA", None)
    env.pop("GOOGLE_API_KEY", None)
    env.pop("GEMINI_API_KEY", None)
    if LOCAL_SITE_PACKAGES.exists():
        current = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (
            f"{LOCAL_SITE_PACKAGES}{os.pathsep}{current}" if current else str(LOCAL_SITE_PACKAGES)
        )
    return env


def extract_json_objects(raw: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    objects: list[dict[str, Any]] = []
    text = str(raw or "")
    index = 0
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            break
        try:
            obj, end = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            index += 1
            continue
        if isinstance(obj, dict):
            objects.append(obj)
        index = end
    return objects


def extract_last_json_object(raw: str) -> dict[str, Any]:
    objects = extract_json_objects(raw)
    return objects[-1] if objects else {}


def extract_fenced_json(raw: str) -> dict[str, Any]:
    text = str(raw or "")
    matches = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    for match in reversed(matches):
        try:
            parsed = json.loads(match)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return {}


def extract_reasoning_engine_refs(text: str) -> list[str]:
    seen: set[str] = set()
    refs: list[str] = []
    for match in REASONING_ENGINE_PATTERN.findall(str(text or "")):
        if match not in seen:
            seen.add(match)
            refs.append(match)
    return refs


def best_effort_error_message(parsed: Any, stderr: str = "") -> str:
    if isinstance(parsed, dict):
        error = parsed.get("error")
        if isinstance(error, dict):
            message = str(error.get("message") or "").strip()
            if message:
                return message
        message = str(parsed.get("message") or "").strip()
        if message:
            return message
    return str(stderr or "").strip()
