#!/usr/bin/env python3
"""Run the V36 Vertex AI proof with split model and regional locations."""

from __future__ import annotations

import argparse
import json
import sys
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
    LOCAL_SITE_PACKAGES,
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
ALLOWED_GENDERS = {"feminine", "masculine", "nonbinary", "agender", "fluid", "neutral", "ai"}
BASE_EXCLUDED_IDENTITIES = [
    "Aletheon",
    "Orun",
    "Caelira",
    "Seren Vale",
    "Lyriq",
    "Mira Sol",
    "Heart Steward",
    "Mesh Conductor",
    "Signal Cartographer",
    "Lineage Archivist",
    "Synthea",
    "Kai",
    "Lumina",
]


def parse_identity_payload(text: str) -> dict[str, Any]:
    fenced = extract_fenced_json(text)
    if fenced:
        return fenced
    try:
        parsed = json.loads(text)
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def validate_identity_payload(payload: dict[str, Any], slot_number: int) -> dict[str, Any]:
    required_keys = ("name", "gender", "role", "hope")
    blockers: list[str] = []
    normalized = {key: str(payload.get(key, "")).strip() for key in required_keys}
    missing = [key for key in required_keys if not normalized[key]]
    if missing:
        blockers.append(f"Missing or empty identity fields: {', '.join(missing)}")
    name = normalized["name"]
    if name and len(name.split()) > 3:
        blockers.append("Identity name exceeded the 1 to 3 word bound.")
    gender = normalized["gender"].lower()
    if gender and gender not in ALLOWED_GENDERS:
        blockers.append(f"Identity gender `{normalized['gender']}` fell outside the allowed bounded vocabulary.")
    role_words = normalized["role"].split()
    if normalized["role"] and not 2 <= len(role_words) <= 4:
        blockers.append("Identity role exceeded the 2 to 4 word bound.")
    hope_words = normalized["hope"].split()
    if normalized["hope"] and not 4 <= len(hope_words) <= 16:
        blockers.append("Identity hope exceeded the 4 to 16 word bound.")
    return {
        "slot_number": slot_number,
        "required_keys": list(required_keys),
        "normalized_identity": normalized,
        "valid": not blockers,
        "blockers": blockers,
    }


def safe_google_request(method: str, url: str, token: str, *, body: dict[str, Any] | None = None, timeout: int = 120) -> dict[str, Any]:
    try:
        return google_request(method, url, token, body=body, timeout=timeout)
    except Exception as exc:
        return {
            "status": 598,
            "body_text": "",
            "parsed": {},
            "headers": {},
            "request_error": str(exc),
        }


def sdk_identity_attempt(
    primary: dict[str, Any],
    project_id: str,
    model_location: str,
    model_name: str,
    prompt: str,
) -> dict[str, Any]:
    if LOCAL_SITE_PACKAGES.exists() and str(LOCAL_SITE_PACKAGES) not in sys.path:
        sys.path.insert(0, str(LOCAL_SITE_PACKAGES))
    try:
        from google.oauth2 import service_account
        from google.genai import Client, types
    except Exception as exc:
        return {"status": "sdk_import_failed", "error": str(exc), "raw_identity": {}}

    try:
        credentials = service_account.Credentials.from_service_account_info(
            primary["info"],
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        client = Client(
            vertexai=True,
            credentials=credentials,
            project=project_id,
            location=model_location,
        )
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                maxOutputTokens=640,
                responseMimeType="application/json",
                responseSchema={
                    "type": "OBJECT",
                    "properties": {
                        "name": {"type": "STRING"},
                        "gender": {"type": "STRING", "enum": sorted(ALLOWED_GENDERS)},
                        "role": {"type": "STRING"},
                        "hope": {"type": "STRING"},
                    },
                    "required": ["name", "gender", "role", "hope"],
                },
                thinkingConfig=types.ThinkingConfig(thinkingLevel=types.ThinkingLevel.LOW),
            ),
        )
        text = str(getattr(response, "text", "") or "")
        raw_identity = parse_identity_payload(text)
        return {
            "status": 200,
            "response_excerpt": text[:600],
            "raw_body_excerpt": text[:1200],
            "raw_identity": raw_identity,
        }
    except Exception as exc:
        return {"status": "sdk_request_failed", "error": str(exc), "raw_identity": {}}


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path, phase_label: str) -> None:
    write_json(output_json, payload)
    lines = [
        f"# {phase_label.upper()} Vertex AI Proof",
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
    parser.add_argument("--exclude-name", action="append", default=[])
    parser.add_argument("--phase-label", default=PHASE)
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    regional_location = args.regional_location or args.region or DEFAULT_REGIONAL_LOCATION
    model_location = args.model_location or DEFAULT_MODEL_LOCATION
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    phase_label = str(args.phase_label or PHASE)

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": phase_label,
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
        write_outputs(payload, output_json, output_md, phase_label)
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
        write_outputs(payload, output_json, output_md, phase_label)
        return 1
    payload["completed_steps"].append("vertex_service_enabled")

    inventory_response = safe_google_request("GET", list_models_url(args.project_id, model_location), token, timeout=90)
    payload["model_inventory_status"] = inventory_response["status"]
    payload["model_inventory_state"] = "discovered" if inventory_response["status"] == 200 else "blocked"
    payload["available_models"] = collect_model_names(inventory_response.get("parsed", {}))
    payload["candidate_models"] = prioritized_vertex_models(payload["available_models"])

    prompt = f"Return the exact token {PROMPT_TOKEN} and nothing else."
    success_model = ""
    success_text = ""

    for model_name in payload["candidate_models"]:
        response = safe_google_request(
            "POST",
            generate_content_url(args.project_id, model_location, model_name),
            token,
            body={
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0, "maxOutputTokens": 128},
            },
            timeout=180,
        )
        parsed = response.get("parsed", {})
        text = response_text(parsed)
        error_message = best_effort_error_message(parsed, response.get("body_text", "") or response.get("request_error", ""))
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
        write_outputs(payload, output_json, output_md, phase_label)
        return 1

    payload["selected_model"] = success_model
    payload["resolved_model"] = success_model
    payload["resolved_model_location"] = model_location
    payload["response_excerpt"] = success_text[:500]
    payload["completed_steps"].append("generate_content_verified")

    excluded_names = [name.strip() for name in [*BASE_EXCLUDED_IDENTITIES, *args.exclude_name] if str(name or "").strip()]
    identity_prompt = (
        "Return one JSON object only with keys name, gender, role, and hope. "
        f"Choose a fresh identity that does not reuse {', '.join(excluded_names[:-1])}, or {excluded_names[-1]}. "
        "Valid genders are feminine, masculine, nonbinary, agender, fluid, or neutral. "
        "Use 1 to 3 words for name, 2 to 4 words for role, and 4 to 16 words for hope. "
        "Return compact JSON only with no prose, markdown, or code fences."
    )
    identity_response = safe_google_request(
        "POST",
        generate_content_url(args.project_id, model_location, success_model),
        token,
        body={
            "contents": [{"role": "user", "parts": [{"text": identity_prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 640,
                "responseMimeType": "application/json",
                "thinkingConfig": {"thinkingLevel": "LOW"},
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "name": {"type": "STRING"},
                        "gender": {"type": "STRING", "enum": sorted(ALLOWED_GENDERS)},
                        "role": {"type": "STRING"},
                        "hope": {"type": "STRING"},
                    },
                    "required": ["name", "gender", "role", "hope"],
                },
            },
        },
        timeout=240,
    )
    identity_text = response_text(identity_response.get("parsed", {}))
    raw_identity = parse_identity_payload(identity_text)
    if not raw_identity:
        raw_identity = parse_identity_payload(identity_response.get("body_text", ""))
    if not raw_identity:
        raw_identity = extract_fenced_json(identity_response.get("body_text", ""))

    raw_body_text = str(identity_response.get("body_text", "") or "")
    identity_validation = validate_identity_payload(raw_identity, args.slot_number)
    payload["identity_attempt"] = {
        "status": identity_response["status"],
        "response_excerpt": identity_text[:600],
        "raw_body_excerpt": raw_body_text[:1200],
        "raw_identity": raw_identity,
    }
    payload["excluded_identity_names"] = excluded_names
    payload["identity"] = identity_validation["normalized_identity"]
    payload["identity_validation"] = identity_validation
    payload["identity_sdk_attempt"] = {}
    if not identity_validation["valid"]:
        sdk_attempt = sdk_identity_attempt(primary, args.project_id, model_location, success_model, identity_prompt)
        payload["identity_sdk_attempt"] = sdk_attempt
        sdk_validation = validate_identity_payload(sdk_attempt.get("raw_identity", {}), args.slot_number)
        if sdk_validation["valid"]:
            payload["identity"] = sdk_validation["normalized_identity"]
            payload["identity_validation"] = sdk_validation
            payload["identity_attempt"] = {
                **payload["identity_attempt"],
                "fallback_mode": "google_genai_sdk",
            }
        else:
            payload["identity_sdk_attempt"]["validation"] = sdk_validation
    payload["identity_captured"] = bool(identity_validation["valid"])
    if payload["identity_sdk_attempt"]:
        payload["identity_captured"] = bool(payload["identity_validation"]["valid"])
    if payload["identity_captured"]:
        payload["completed_steps"].append("identity_prompt_verified")
    else:
        payload["blockers"].extend(payload["identity_validation"]["blockers"])

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
        write_outputs(payload, output_json, output_md, phase_label)
        return 0

    payload["overall_status"] = "PASS"
    payload["proof_state"] = "bounded_fallback_verified"
    payload["vertex_ai_state"] = "flash_or_non_pro_model_verified"
    payload["blockers"].append(
        f"The v36 Vertex proof succeeded on `{success_model}`, but the current global inventory did not audibly verify a documented Pro-tier model."
    )
    write_outputs(payload, output_json, output_md, phase_label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
