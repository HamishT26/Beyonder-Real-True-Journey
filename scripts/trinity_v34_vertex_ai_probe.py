#!/usr/bin/env python3
"""Run the bounded V34 Vertex AI proof with highest-available Pro-tier discovery."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v34_cloud_common import (
    FLASH_FALLBACK_MODEL,
    PHASE,
    PRIMARY_REGION,
    PROJECT_ID,
    TRACE_DIR,
    VERTEX_SERVICE_NAME,
    collect_model_names,
    ensure_service_enabled,
    generate_content_url,
    list_models_url,
    load_primary_service_account,
    google_request,
    mask_email,
    now_iso,
    prioritized_vertex_models,
    response_text,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = TRACE_DIR / "v34-vertex-ai-proof-v1.json"
OUTPUT_MD = TRACE_DIR / "v34-vertex-ai-proof-v1.md"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V34 Vertex AI Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Vertex AI state: `{payload.get('vertex_ai_state', 'unknown')}`",
        f"- Primary identity: `{payload.get('primary_identity', '') or 'unknown'}`",
        f"- Preferred region: `{payload.get('preferred_region', '') or 'unknown'}`",
        f"- Selected model: `{payload.get('selected_model', '') or 'unresolved'}`",
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
    parser = argparse.ArgumentParser(description="Run the bounded V34 Vertex AI proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--fallback-model", default=FLASH_FALLBACK_MODEL)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "proof_state": "pending",
        "vertex_ai_state": "pending",
        "project_id": args.project_id,
        "preferred_region": args.region,
        "fallback_model": args.fallback_model,
        "completed_steps": [],
        "blockers": [],
        "attempts": [],
        "available_models": [],
    }

    try:
        _bundle, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["proof_state"] = "missing_primary_service_account"
        payload["vertex_ai_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload)
        return 1

    token = minted["token"]
    payload["primary_identity"] = mask_email(primary["client_email"])
    payload["completed_steps"].append("mint_primary_token")

    service = ensure_service_enabled(args.project_id, token, VERTEX_SERVICE_NAME)
    payload["service_enablement"] = service
    if service["final_status"] != 200 or service["final_state"] != "ENABLED":
        payload["proof_state"] = "service_enablement_blocked"
        payload["vertex_ai_state"] = "blocked_service_enablement"
        payload["blockers"].append("Vertex AI service usage did not report `ENABLED` after the bounded enablement pass.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    inventory_response = google_request("GET", list_models_url(args.project_id, args.region), token, timeout=90)

    if inventory_response is not None:
        payload["model_inventory_status"] = inventory_response["status"]
        available_models = collect_model_names(inventory_response.get("parsed", {}))
        payload["available_models"] = available_models
        payload["model_inventory_excerpt"] = available_models[:20]
        payload["model_inventory_state"] = "discovered" if inventory_response["status"] == 200 else "blocked"
    else:
        available_models = []
        payload["model_inventory_state"] = "blocked"

    candidates = prioritized_vertex_models(available_models, fallback_model=args.fallback_model)[:5]
    if not candidates:
        candidates = [args.fallback_model]
    payload["candidate_models"] = candidates

    prompt = "Return the exact token V34_VERTEX_OK and nothing else."
    for model_name in candidates:
        response = google_request(
            "POST",
            generate_content_url(args.project_id, args.region, model_name),
            token,
            body={
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}],
                    }
                ],
                "generationConfig": {"temperature": 0, "maxOutputTokens": 64},
            },
            timeout=120,
        )
        parsed = response.get("parsed", {})
        text = response_text(parsed)
        attempt = {
            "model_name": model_name,
            "http_status": response["status"],
            "response_excerpt": text[:500],
            "finish_reason": "",
            "raw_model_version": parsed.get("modelVersion", "") if isinstance(parsed, dict) else "",
            "is_fallback": model_name == args.fallback_model,
        }
        candidates_list = parsed.get("candidates", []) if isinstance(parsed, dict) else []
        if isinstance(candidates_list, list) and candidates_list:
            attempt["finish_reason"] = str(candidates_list[0].get("finishReason", ""))
        payload["attempts"].append(attempt)
        if response["status"] == 200 and "V34_VERTEX_OK" in text:
            payload["resolved_region"] = args.region
            payload["selected_model"] = model_name
            payload["resolved_model"] = model_name
            payload["usage_metadata"] = parsed.get("usageMetadata", {}) if isinstance(parsed, dict) else {}
            payload["response_excerpt"] = text[:500]
            payload["completed_steps"].append("generate_content_verified")
            payload["vertex_ai_state"] = (
                "flash_fallback_verified" if model_name == args.fallback_model else "pro_tier_model_verified"
            )
            payload["overall_status"] = "PASS"
            payload["proof_state"] = "highest_available_model_verified" if model_name != args.fallback_model else "flash_fallback_verified"
            if payload.get("model_inventory_state") != "discovered" and model_name == args.fallback_model:
                payload["blockers"].append("Model inventory discovery was unavailable, so the proof fell back to the bounded flash model path.")
            write_outputs(payload)
            return 0

    payload["proof_state"] = "no_supported_model_resolved"
    payload["vertex_ai_state"] = "blocked_model_resolution"
    payload["blockers"].append(
        "No candidate Google model returned a successful `generateContent` response in the bounded region/model pass."
    )
    write_outputs(payload)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
