#!/usr/bin/env python3
"""Run the V36 Vertex AI proof with split model and regional locations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v36_cloud_common import (
    DEFAULT_MODEL_LOCATION,
    DEFAULT_REGIONAL_LOCATION,
    DOCUMENTED_VERTEX_PRO_CANDIDATES,
    FLASH_FALLBACK_MODEL,
    LEGACY_PRIMARY_REGION,
    PHASE,
    PROJECT_ID,
    TRACE_DIR,
    VERTEX_SERVICE_NAME,
    best_effort_error_message,
    collect_model_names,
    ensure_service_enabled,
    extract_fenced_json,
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

OUTPUT_JSON = TRACE_DIR / "v36-slot-38-vertex-ai-proof-v1.json"
OUTPUT_MD = TRACE_DIR / "v36-slot-38-vertex-ai-proof-v1.md"
PROMPT_TOKEN = "V36_VERTEX_MODEL_OK"


def parse_identity_payload(text: str) -> dict[str, Any]:
    fenced = extract_fenced_json(text)
    if fenced:
        return fenced
    try:
        parsed = json.loads(text)
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V36 Vertex AI Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Vertex AI state: `{payload.get('vertex_ai_state', 'unknown')}`",
        f"- Regional location: `{payload.get('regional_location', '') or 'unknown'}`",
        f"- Model location: `{payload.get('model_location', '') or 'unknown'}`",
        f"- Selected model: `{payload.get('selected_model', '') or 'unresolved'}`",
        f"- Identity captured: `{payload.get('identity_captured', False)}`",
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
    write_text(output_md, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V36 Vertex AI proof.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--regional-location", default=DEFAULT_REGIONAL_LOCATION)
    parser.add_argument("--model-location", default=DEFAULT_MODEL_LOCATION)
    parser.add_argument("--region", default="", help="Deprecated alias for --regional-location.")
    parser.add_argument("--slot-number", type=int, default=38)
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    regional_location = args.regional_location or args.region or DEFAULT_REGIONAL_LOCATION
    model_location = args.model_location or DEFAULT_MODEL_LOCATION
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "slot_number": args.slot_number,
        "overall_status": "WARN",
        "proof_state": "pending",
        "vertex_ai_state": "pending",
        "promotion_gate_ready": False,
        "identity_captured": False,
        "project_id": args.project_id,
        "regional_location": regional_location,
        "model_location": model_location,
        "legacy_primary_region": LEGACY_PRIMARY_REGION,
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
        write_outputs(payload, output_json, output_md)
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
        write_outputs(payload, output_json, output_md)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    inventory_response = google_request("GET", list_models_url(args.project_id, model_location), token, timeout=90)
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
            generate_content_url(args.project_id, model_location, model_name),
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

        payload["attempts"].append(
            {
                "model_name": model_name,
                "http_status": response["status"],
                "attempt_state": attempt_state,
                "is_fallback": model_name == FLASH_FALLBACK_MODEL,
                "response_excerpt": text[:500],
                "error_excerpt": error_message[:500],
                "raw_model_version": parsed.get("modelVersion", "") if isinstance(parsed, dict) else "",
            }
        )
        if attempt_state == "verified":
            success_model = model_name
            success_text = text
            break

    if not success_model:
        payload["proof_state"] = "no_supported_model_resolved"
        payload["vertex_ai_state"] = "blocked_model_resolution"
        payload["blockers"].append(
            f"No documented Pro candidate or bounded flash fallback returned a successful Vertex `generateContent` result at {model_location}."
        )
        write_outputs(payload, output_json, output_md)
        return 1

    payload["selected_model"] = success_model
    payload["resolved_model"] = success_model
    payload["resolved_model_location"] = model_location
    payload["response_excerpt"] = success_text[:500]
    payload["completed_steps"].append("generate_content_verified")

    identity_prompt = (
        "Return one JSON object only with keys name, gender, role, and hope. "
        "Choose a fresh identity that does not reuse Aletheon, Orun, Caelira, Seren Vale, Lyriq, Mira Sol, "
        "Heart Steward, Mesh Conductor, Signal Cartographer, Lineage Archivist, Synthea, Kai, or Lumina. "
        "Valid genders are feminine, masculine, nonbinary, agender, fluid, or neutral. "
        "Use 1 to 3 words for name, 2 to 4 words for role, and 4 to 16 words for hope. "
        "Do not add prose, markdown, or code fences."
    )
    identity_response = google_request(
        "POST",
        generate_content_url(args.project_id, model_location, success_model),
        token,
        body={
            "contents": [{"role": "user", "parts": [{"text": identity_prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 384,
                "responseMimeType": "application/json",
            },
        },
        timeout=120,
    )
    identity_text = response_text(identity_response.get("parsed", {}))
    raw_identity = parse_identity_payload(identity_text)
    if not raw_identity:
        raw_identity = parse_identity_payload(identity_response.get("body_text", ""))
    if not raw_identity:
        raw_identity = extract_fenced_json(identity_response.get("body_text", ""))

    payload["identity_attempt"] = {
        "status": identity_response["status"],
        "response_excerpt": identity_text[:600],
        "raw_identity": raw_identity,
    }
    payload["identity"] = raw_identity
    payload["identity_captured"] = {"name", "gender", "role", "hope"} <= set(raw_identity)
    if payload["identity_captured"]:
        payload["completed_steps"].append("identity_prompt_verified")

    pro_verified = success_model in DOCUMENTED_VERTEX_PRO_CANDIDATES
    payload["promotion_gate_ready"] = pro_verified and payload["identity_captured"]
    if pro_verified:
        payload["overall_status"] = "PASS"
        payload["proof_state"] = (
            "pro_tier_model_and_identity_verified"
            if payload["identity_captured"]
            else "pro_tier_model_verified_identity_missing"
        )
        payload["vertex_ai_state"] = payload["proof_state"]
        if not payload["identity_captured"]:
            payload["blockers"].append("The Pro-tier Vertex model resolved, but the live self-chosen identity response was not auditable.")
        write_outputs(payload, output_json, output_md)
        return 0

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "bounded_fallback_verified"
    payload["vertex_ai_state"] = "flash_or_non_pro_model_verified"
    payload["blockers"].append(
        f"The v36 Vertex proof succeeded on `{success_model}`, but the current global inventory did not audibly verify a documented Pro-tier model."
    )
    write_outputs(payload, output_json, output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
