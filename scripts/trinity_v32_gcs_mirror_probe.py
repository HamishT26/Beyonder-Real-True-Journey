#!/usr/bin/env python3
"""Create and verify the bounded V32 primary GCS mirror lane."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

from trinity_v32_runtime_common import (
    DEFAULT_GCP_KEY_BUNDLE,
    LOCAL_RUNTIME,
    PRIMARY_BUCKET_PREFIX,
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
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-gcs-primary-mirror-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-gcs-primary-mirror-proof-v1.md"


def ensure_bucket(project_id: str, token: str, bucket_name: str, region: str) -> dict[str, Any]:
    probe = google_request("GET", f"https://storage.googleapis.com/storage/v1/b/{bucket_name}", token)
    if probe["status"] == 200:
        return {"bucket_name": bucket_name, "status": "exists", "http_status": 200}
    create = google_request(
        "POST",
        f"https://storage.googleapis.com/storage/v1/b?project={project_id}",
        token,
        body={
            "name": bucket_name,
            "location": region.upper(),
            "storageClass": "STANDARD",
            "versioning": {"enabled": True},
            "labels": {"phase": "v32omega", "managed_by": "codex"},
        },
    )
    return {
        "bucket_name": bucket_name,
        "status": "created" if create["status"] in {200, 201} else "blocked",
        "http_status": create["status"],
        "error": create.get("parsed", {}),
    }


def upload_text_object(bucket_name: str, token: str, object_name: str, content: str) -> dict[str, Any]:
    return google_request(
        "POST",
        "https://storage.googleapis.com/upload/storage/v1"
        f"/b/{bucket_name}/o?uploadType=media&name={object_name}",
        token,
        raw_body=content.encode("utf-8"),
        headers={"Content-Type": "text/markdown"},
    )


def read_text_object(bucket_name: str, token: str, object_name: str) -> dict[str, Any]:
    return google_request(
        "GET",
        f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o/{quote(object_name, safe='')}?alt=media",
        token,
    )


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 GCS Primary Mirror Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Bucket: `{payload.get('bucket_name', '') or 'unknown'}`",
        f"- Primary identity: `{payload.get('primary_identity', '') or 'unknown'}`",
        "",
        "## Steps",
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
    parser = argparse.ArgumentParser(description="Create and verify the bounded V32 GCS mirror.")
    parser.add_argument("--bundle", default=str(DEFAULT_GCP_KEY_BUNDLE))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--bucket-prefix", default=PRIMARY_BUCKET_PREFIX)
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "WARN",
        "proof_state": "pending",
        "project_id": args.project_id,
        "region": args.region,
        "completed_steps": [],
        "blockers": [],
    }

    bundle = load_gcp_service_accounts(Path(args.bundle))
    records = {row["alias"]: row for row in bundle["records"]}
    primary = records.get("compute_default") or records.get("app_engine_default")
    if primary is None:
        payload["proof_state"] = "missing_primary_service_account"
        payload["blockers"].append("No compute_default or app_engine_default service account was available.")
        write_outputs(payload)
        return 1

    minted = mint_access_token(primary["info"])
    token = minted["token"]
    payload["primary_identity"] = mask_email(primary["client_email"])
    payload["completed_steps"].append("mint_primary_token")

    bucket_name = args.bucket_prefix
    ensure = ensure_bucket(args.project_id, token, bucket_name, args.region)
    if ensure["status"] == "blocked" and ensure.get("http_status") == 409:
        suffix = datetime.now(timezone.utc).strftime("%H%M%S").lower()
        bucket_name = f"{args.bucket_prefix}-{suffix}"
        ensure = ensure_bucket(args.project_id, token, bucket_name, args.region)
    payload["bucket_name"] = bucket_name
    payload["bucket_result"] = ensure
    if ensure["status"] not in {"created", "exists"}:
        payload["proof_state"] = "bucket_creation_blocked"
        payload["blockers"].append(f"GCS bucket bootstrap failed with HTTP {ensure['http_status']}.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("ensure_bucket")

    object_name = f"proofs/v32-primary-mirror-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.md"
    manifest_name = "manifests/v32-primary-mirror-manifest.json"
    runtime_dir = LOCAL_RUNTIME / "gcs"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    mirror_manifest = {
        "generated_utc": now_iso(),
        "authority_model": "repo_first",
        "bucket_name": bucket_name,
        "allowed_families": [
            "docs/memory-archives",
            "docs/trinity-live-traces",
            "docs/auto-generated",
        ],
        "notes": [
            "The authoritative repo remains outside OneDrive.",
            "The GCS primary mirror is bounded to archives and reports unless explicitly widened later.",
        ],
    }
    manifest_path = runtime_dir / "v32-primary-mirror-manifest.json"
    manifest_path.write_text(json.dumps(mirror_manifest, indent=2) + "\n", encoding="utf-8")

    proof_text = (
        "# V32 GCS Primary Mirror Proof\n\n"
        f"- generated_utc: {now_iso()}\n"
        f"- bucket: {bucket_name}\n"
        "- purpose: bounded cloud mirror verification\n"
    )
    upload = upload_text_object(bucket_name, token, object_name, proof_text)
    manifest_upload = upload_text_object(bucket_name, token, manifest_name, manifest_path.read_text(encoding="utf-8"))
    payload["upload_result"] = {"object_name": object_name, "status": upload["status"]}
    payload["manifest_upload_result"] = {"object_name": manifest_name, "status": manifest_upload["status"]}
    if upload["status"] != 200 or manifest_upload["status"] != 200:
        payload["proof_state"] = "upload_blocked"
        payload["blockers"].append("Bucket exists, but upload verification did not complete cleanly.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("upload_verification_objects")

    readback = read_text_object(bucket_name, token, object_name)
    manifest_readback = read_text_object(bucket_name, token, manifest_name)
    payload["readback_status"] = readback["status"]
    payload["manifest_readback_status"] = manifest_readback["status"]
    payload["artifact_content_matches"] = readback.get("body_text", "") == proof_text
    payload["manifest_content_matches"] = manifest_readback.get("body_text", "") == manifest_path.read_text(encoding="utf-8")
    if readback["status"] == 200 and manifest_readback["status"] == 200 and payload["artifact_content_matches"] and payload["manifest_content_matches"]:
        payload["completed_steps"].append("readback_verification")
        payload["overall_status"] = "PASS"
        payload["proof_state"] = "primary_mirror_verified"
        payload["gcs_primary_mirror_state"] = "bounded_primary_mirror_verified"
    else:
        payload["proof_state"] = "readback_blocked"
        payload["blockers"].append("Uploaded mirror proof object did not read back cleanly.")

    write_outputs(payload)
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
