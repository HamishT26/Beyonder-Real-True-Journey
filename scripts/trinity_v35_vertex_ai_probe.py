#!/usr/bin/env python3
"""Run the V35 Vertex AI proof with explicit Pro-tier attempts in Sydney."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v35_cloud_common import (
    DOCUMENTED_VERTEX_PRO_CANDIDATES,
    FLASH_FALLBACK_MODEL,
    PHASE,
    PRIMARY_REGION,
    PROJECT_ID,
    TRACE_DIR,
    VERTEX_SERVICE_NAME,
    best_effort_error_message,
    collect_model_names,
    ensure_service_enabled,
    generate_content_url,
    google_request,
    list_models_url,
    load_primary_service_account,
    now_iso,
    primary_identity_fields,
    prioritized_vertex_models,
    response_text,
    write_json,
    write_text,
)

OUTPUT_JSON = TRACE_DIR / "v35-vertex-ai-proof-v1.json"
OUTPUT_MD = TRACE_DIR / "v35-vertex-ai-proof-v1.md"
PROMPT_TOKEN = "V35_VERTEX_MODEL_OK"


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V35 Vertex AI Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Vertex AI state: `{payload.get('vertex_ai_state', 'unknown')}`",
        f"- Preferred region: `{payload.get('preferred_region', '') or 'unknown'}`",
        f"- Selected model: `{payload.get('selected_model', '') or 'unresolved'}`",
        f"- Promotion gate ready: `{payload.get('promotion_gate_ready', False)}`",
        "",
        "## Completed Steps",
        "",
    ]
    for step in payload.get("completed_steps", []):
        lines.append(f"- `{step}`")
    if payload.get("attempts"):
        lines.extend(["", "## Model Attempts", ""])
        for attempt in payload["attempts"]:
            lines.append(
                f"- `{attempt['model_name']}` -> status `{attempt['http_status']}` / state `{attempt['attempt_state']}`"
            )
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V35 Vertex AI proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "proof_state": "pending",
        "vertex_ai_state": "pending",
        "promotion_gate_ready": False,
        "project_id": args.project_id,
        "preferred_region": args.region,
        "documented_pro_candidates": DOCUMENTED_VERTEX_PRO_CANDIDATES,
        "fallback_model": FLASH_FALLBACK_MODEL,
        "completed_steps": [],
        "blockers": [],
        "attempts": [],
        "available_models": [],
    }

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["proof_state"] = "missing_primary_service_account"
        payload["vertex_ai_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload)
        return 1

    payload.update(primary_identity_fields(primary, minted))
    token = minted["token"]
    payload["completed_steps"].append("mint_primary_token")

    service = ensure_service_enabled(args.project_id, token, VERTEX_SERVICE_NAME)
    payload["service_enablement"] = service
    if service["final_status"] != 200 or service["final_state"] != "ENABLED":
        payload["proof_state"] = "service_enablement_blocked"
        payload["vertex_ai_state"] = "blocked_service_enablement"
        payload["blockers"].append("Vertex AI did not report `ENABLED` after the bounded service check.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    inventory_response = google_request("GET", list_models_url(args.project_id, args.region), token, timeout=90)
    payload["model_inventory_status"] = inventory_response["status"]
    payload["model_inventory_state"] = "discovered" if inventory_response["status"] == 200 else "blocked"
    payload["available_models"] = collect_model_names(inventory_response.get("parsed", {}))
    payload["candidate_models"] = prioritized_vertex_models(payload["available_models"])

    prompt = f"Return the exact token {PROMPT_TOKEN} and nothing else."
    success_model = ""
    success_text = ""

    for model_name in payload["candidate_models"]:
        response = google_request(
            "POST",
            generate_content_url(args.project_id, args.region, model_name),
            token,
            body={
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0, "maxOutputTokens": 128},
            },
            timeout=120,
        )
        parsed = response.get("parsed", {})
        text = response_text(parsed)
        error_message = best_effort_error_message(parsed, response.get("body_text", ""))
        attempt_state = "error"
        if response["status"] == 200 and PROMPT_TOKEN in text:
            attempt_state = "verified"
        elif response["status"] == 404:
            attempt_state = "not_exposed"
        elif response["status"] in {401, 403}:
            attempt_state = "auth_blocked"

        attempt = {
            "model_name": model_name,
            "http_status": response["status"],
            "attempt_state": attempt_state,
            "is_fallback": model_name == FLASH_FALLBACK_MODEL,
            "response_excerpt": text[:500],
            "error_excerpt": error_message[:500],
            "raw_model_version": parsed.get("modelVersion", "") if isinstance(parsed, dict) else "",
        }
        payload["attempts"].append(attempt)

        if attempt_state == "verified":
            success_model = model_name
            success_text = text
            break

    if success_model:
        payload["selected_model"] = success_model
        payload["resolved_model"] = success_model
        payload["resolved_region"] = args.region
        payload["response_excerpt"] = success_text[:500]
        payload["completed_steps"].append("generate_content_verified")
        pro_verified = success_model in DOCUMENTED_VERTEX_PRO_CANDIDATES
        payload["promotion_gate_ready"] = pro_verified
        if pro_verified:
            payload["overall_status"] = "PASS"
            payload["proof_state"] = "pro_tier_model_verified"
            payload["vertex_ai_state"] = "pro_tier_model_verified"
        else:
            payload["overall_status"] = "PASS"
            payload["proof_state"] = "flash_fallback_verified"
            payload["vertex_ai_state"] = "flash_fallback_verified"
            payload["blockers"].append(
                "Sydney Vertex proof succeeded only on `gemini-2.5-flash`; no Pro-tier Gemini model was auditable for full slot-38 promotion."
            )
        write_outputs(payload)
        return 0

    payload["proof_state"] = "no_supported_model_resolved"
    payload["vertex_ai_state"] = "blocked_model_resolution"
    payload["blockers"].append(
        "No documented Pro candidate or bounded flash fallback returned a successful Vertex `generateContent` result in australia-southeast1."
    )
    write_outputs(payload)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
