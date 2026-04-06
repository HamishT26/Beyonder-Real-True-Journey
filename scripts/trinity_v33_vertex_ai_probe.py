#!/usr/bin/env python3
"""Run a bounded Vertex AI publisher-model proof via direct REST."""

from __future__ import annotations

import argparse
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
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v33-vertex-ai-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v33-vertex-ai-proof-v1.md"
SERVICE_NAME = "aiplatform.googleapis.com"
MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash",
    "gemini-1.5-flash-002",
    "gemini-1.5-flash-001",
]


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


def generate_content_url(project_id: str, region: str, model_name: str) -> str:
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/"
        f"publishers/google/models/{model_name}:generateContent"
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


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V33 Vertex AI Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Vertex AI state: `{payload.get('vertex_ai_state', 'unknown')}`",
        f"- Primary identity: `{payload.get('primary_identity', '') or 'unknown'}`",
        f"- Resolved region: `{payload.get('resolved_region', '') or 'unresolved'}`",
        f"- Resolved model: `{payload.get('resolved_model', '') or 'unresolved'}`",
        "",
        "## Completed Steps",
        "",
    ]
    for step in payload.get("completed_steps", []):
        lines.append(f"- `{step}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded Vertex AI REST proof.")
    parser.add_argument("--bundle", default=str(DEFAULT_GCP_KEY_BUNDLE))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--primary-region", default=PRIMARY_REGION)
    parser.add_argument("--fallback-region", default="us-central1")
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v33_omega",
        "overall_status": "WARN",
        "proof_state": "pending",
        "vertex_ai_state": "pending",
        "project_id": args.project_id,
        "preferred_regions": [args.primary_region, args.fallback_region],
        "completed_steps": [],
        "blockers": [],
        "model_candidates": MODEL_CANDIDATES,
        "attempts": [],
    }

    bundle = load_gcp_service_accounts(Path(args.bundle))
    records = {row["alias"]: row for row in bundle["records"]}
    primary = records.get("compute_default") or records.get("app_engine_default")
    if primary is None:
        payload["proof_state"] = "missing_primary_service_account"
        payload["vertex_ai_state"] = "blocked_missing_identity"
        payload["blockers"].append("No primary GCP service account was available for the Vertex AI probe.")
        write_outputs(payload)
        return 1

    minted = mint_access_token(primary["info"])
    token = minted["token"]
    payload["primary_identity"] = mask_email(primary["client_email"])
    payload["completed_steps"].append("mint_primary_token")

    service = ensure_service_enabled(args.project_id, token, SERVICE_NAME)
    payload["service_enablement"] = service
    if service["final_status"] != 200 or service["final_state"] != "ENABLED":
        payload["proof_state"] = "service_enablement_blocked"
        payload["vertex_ai_state"] = "blocked_service_enablement"
        payload["blockers"].append("Vertex AI service usage did not report `ENABLED` after the bounded enablement pass.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    prompt = "Return the exact token V33_VERTEX_OK and nothing else."
    for region in [args.primary_region, args.fallback_region]:
        for model_name in MODEL_CANDIDATES:
            response = google_request(
                "POST",
                generate_content_url(args.project_id, region, model_name),
                token,
                body={
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": prompt}],
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0,
                        "maxOutputTokens": 64,
                    },
                },
                timeout=120,
            )
            parsed = response.get("parsed", {})
            text = response_text(parsed)
            attempt = {
                "region": region,
                "model_name": model_name,
                "http_status": response["status"],
                "response_excerpt": text[:500],
                "finish_reason": "",
                "error": parsed.get("error", {}) if isinstance(parsed, dict) else {},
            }
            candidates = parsed.get("candidates", []) if isinstance(parsed, dict) else []
            if isinstance(candidates, list) and candidates:
                attempt["finish_reason"] = str(candidates[0].get("finishReason", ""))
            payload["attempts"].append(attempt)
            if response["status"] == 200 and "V33_VERTEX_OK" in text:
                payload["resolved_region"] = region
                payload["resolved_model"] = model_name
                payload["usage_metadata"] = parsed.get("usageMetadata", {}) if isinstance(parsed, dict) else {}
                payload["response_excerpt"] = text[:500]
                payload["raw_model_response"] = {
                    "finish_reason": attempt["finish_reason"],
                    "model_version": parsed.get("modelVersion", "") if isinstance(parsed, dict) else "",
                }
                payload["completed_steps"].append("generate_content_verified")
                payload["overall_status"] = "PASS"
                payload["proof_state"] = "publisher_model_generate_content_verified"
                payload["vertex_ai_state"] = "generate_content_verified"
                write_outputs(payload)
                return 0

    payload["proof_state"] = "no_supported_flash_model_resolved"
    payload["vertex_ai_state"] = "blocked_model_resolution"
    payload["blockers"].append("No candidate Google Flash model returned a successful `generateContent` response in the bounded region/model pass.")
    write_outputs(payload)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
