#!/usr/bin/env python3
"""Shared helpers for the bounded V34 cloud proof lanes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import (
    DEFAULT_GCP_KEY_BUNDLE,
    PRIMARY_REGION,
    PROJECT_ID,
    google_request,
    load_gcp_service_accounts,
    mask_email,
    mint_access_token,
    now_iso,
    run_cmd,
    temp_file,
    temp_kubeconfig,
    windows_kubectl,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v34_omega"
VERTEX_SERVICE_NAME = "aiplatform.googleapis.com"
BIGTABLE_SERVICE_NAMES = ["bigtableadmin.googleapis.com", "bigtable.googleapis.com"]
FLASH_FALLBACK_MODEL = "gemini-2.5-flash"
PRO_MODEL_PREFIXES = ["gemini-3-pro", "gemini-2.5-pro", "gemini-2.0-pro", "gemini-1.5-pro"]
MEMORY_BANK_REGIONS = [PRIMARY_REGION, "us-central1"]


def service_url(project_id: str, service_name: str) -> str:
    return f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services/{service_name}"


def ensure_service_enabled(project_id: str, token: str, service_name: str) -> dict[str, Any]:
    initial = google_request("GET", service_url(project_id, service_name), token, timeout=60)
    initial_state = str(initial.get("parsed", {}).get("state", "UNKNOWN"))
    enable_attempted = False
    enable_response: dict[str, Any] | None = None
    final = initial
    if initial_state != "ENABLED":
        enable_attempted = True
        enable_response = google_request("POST", f"{service_url(project_id, service_name)}:enable", token, body={}, timeout=120)
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


def load_primary_service_account(bundle_path: Path | str = DEFAULT_GCP_KEY_BUNDLE) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    bundle = load_gcp_service_accounts(Path(bundle_path))
    records = {row["alias"]: row for row in bundle["records"]}
    primary = records.get("compute_default") or records.get("app_engine_default")
    if primary is None:
        raise RuntimeError("No primary GCP service account was available for the v34 proof lane.")
    minted = mint_access_token(primary["info"])
    return bundle, primary, minted


def generate_content_url(project_id: str, region: str, model_name: str) -> str:
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/"
        f"publishers/google/models/{model_name}:generateContent"
    )


def list_models_url(project_id: str, region: str) -> str:
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/"
        "publishers/google/models?pageSize=100"
    )


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
                ):
                    add(item)
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str):
            if "/models/" in value or value.startswith("gemini-"):
                add(value)

    walk(payload)
    return names


def model_rank(model_name: str) -> tuple[int, str]:
    lowered = normalize_model_name(model_name).lower()
    for index, prefix in enumerate(PRO_MODEL_PREFIXES):
        if lowered.startswith(prefix):
            return (index, lowered)
    if lowered.startswith(FLASH_FALLBACK_MODEL):
        return (len(PRO_MODEL_PREFIXES), lowered)
    return (len(PRO_MODEL_PREFIXES) + 1, lowered)


def prioritized_vertex_models(available_models: list[str], fallback_model: str = FLASH_FALLBACK_MODEL) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for model in available_models:
        normalized = normalize_model_name(model)
        if normalized and normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)
    ordered.sort(key=model_rank)
    if fallback_model not in seen:
        ordered.append(fallback_model)
    return ordered


def kubectl_json(kubectl_path: str, kubeconfig: Path, args: list[str], timeout: int = 180) -> dict[str, Any]:
    result = run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), *args], timeout=timeout)
    parsed: Any = {}
    if result.stdout.strip():
        try:
            import json

            parsed = json.loads(result.stdout)
        except Exception:
            parsed = {"raw_stdout": result.stdout.strip()}
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "parsed": parsed,
    }


def kubectl_text(kubectl_path: str, kubeconfig: Path, args: list[str], timeout: int = 180) -> dict[str, Any]:
    result = run_cmd([kubectl_path, "--kubeconfig", str(kubeconfig), *args], timeout=timeout)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def ensure_namespace(kubectl_path: str, kubeconfig: Path, namespace: str) -> dict[str, Any]:
    existing = kubectl_text(kubectl_path, kubeconfig, ["get", "namespace", namespace, "-o", "name"], timeout=90)
    if existing["returncode"] == 0:
        return {"status": "exists", **existing}
    created = kubectl_text(kubectl_path, kubeconfig, ["create", "namespace", namespace], timeout=90)
    if created["returncode"] == 0:
        return {"status": "created", **created}
    return {"status": "blocked", **created}


def primary_identity_fields(primary: dict[str, Any], minted: dict[str, Any]) -> dict[str, Any]:
    return {
        "primary_identity": mask_email(primary["client_email"]),
        "token_expiry_utc": minted.get("expiry_utc", ""),
        "token_scopes": minted.get("scopes", []),
    }
