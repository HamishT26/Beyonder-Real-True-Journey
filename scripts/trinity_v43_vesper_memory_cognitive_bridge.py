#!/usr/bin/env python3
"""Write bounded V43 telemetry to Bigtable and prove a minimal Discovery Engine cognitive lane when available."""

from __future__ import annotations

import argparse
import base64
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import PROJECT_ID
from trinity_v36_cloud_common import load_primary_service_account, primary_identity_fields
from trinity_v37_slot38_memory_bridge import ensure_v37_bigtable_imports
from trinity_v43_common import now_iso, read_json, resolve_status, to_jsonable, write_json, write_text, ROOT

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-vesper-memory-cognitive-bridge-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v43-vesper-memory-cognitive-bridge-v1.md"
DEFAULT_INSTANCE_ID = "beyonder-v37-slot38-dev"
DEFAULT_TABLE_ID = "v43_omega_runtime"
DEFAULT_COLUMN_FAMILY = "cf1"
DEFAULT_LOCATION = "global"
DEFAULT_DATASTORE_ID = "v43-cognitive-store"
DEFAULT_DOCUMENT_ID = "v43-telemetry-marker"
BIGTABLE_SERVICES = ("bigtableadmin.googleapis.com", "bigtable.googleapis.com")
TELEMETRY_SOURCES = (
    "docs/trinity-live-traces/v43-cloud-carry-forward-v1.json",
    "docs/trinity-live-traces/v43-kai-orchestration-bridge-v1.json",
    "docs/trinity-live-traces/v43-gmut-lab-bundle-v1.json",
    "docs/trinity-live-traces/v43-wsl-resurrection-v1.json",
    "docs/trinity-live-traces/v43-google-drive-proof-v1.json",
    "docs/trinity-live-traces/v43-codex-capability-audit-v1.json",
    "docs/trinity-live-traces/v43-automation-registry-v1.json",
)


def _summary(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    payload = read_json(path)
    summary = {
        "path": rel_path,
        "present": path.exists(),
        "overall_status": resolve_status(payload),
    }
    for key in (
        "api_ascendancy_state",
        "cloud_run_state",
        "cloud_build_state",
        "dataplex_state",
        "automation_backend_state",
        "google_drive_state",
        "filesystem_promotion_state",
        "wsl_recovery_state",
        "vesper_cognitive_engine_state",
        "gmut_experiment_state",
        "kai_orchestration_state",
    ):
        if key in payload:
            summary[key] = payload[key]
    return summary


def _http_json(method: str, url: str, token: str, *, body: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, method=method, headers=headers, data=data)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = response.read().decode("utf-8", errors="replace")
            parsed = json.loads(raw) if raw else {}
            return {"ok": True, "status_code": response.status, "body": parsed, "raw": raw}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return {"ok": False, "status_code": exc.code, "body": parsed, "raw": raw}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "status_code": 0, "body": {"error": str(exc)}, "raw": str(exc)}


def _poll_operation(operation_name: str, token: str) -> dict[str, Any]:
    url = f"https://discoveryengine.googleapis.com/v1/{operation_name}"
    polls: list[dict[str, Any]] = []
    for _ in range(30):
        response = _http_json("GET", url, token)
        polls.append({"status_code": response["status_code"], "body": response["body"]})
        if response["ok"] and bool(response["body"].get("done")):
            return {"state": "done", "final": response, "polls": polls}
        time.sleep(5)
    return {"state": "timeout", "final": polls[-1] if polls else {}, "polls": polls}


def _ensure_bigtable_table(project_id: str, bundle_path: Path, instance_id: str, table_id: str, telemetry: dict[str, Any]) -> dict[str, Any]:
    try:
        Client, _enums, MaxVersionsGCRule, service_account = ensure_v37_bigtable_imports()
        from google.auth.transport.requests import Request  # type: ignore

        _records, primary, _minted = load_primary_service_account(bundle_path)
        credentials = service_account.Credentials.from_service_account_info(
            primary["info"],
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        credentials.refresh(Request())
        client = Client(project=project_id, credentials=credentials, admin=True)
        instance = client.instance(instance_id)
        if not instance.exists():
            return {
                "state": "blocked_proven_instance_missing",
                "blocker": f"The proven Bigtable instance `{instance_id}` does not exist.",
            }

        table = instance.table(table_id)
        table_created = False
        if not table.exists():
            table.create(column_families={DEFAULT_COLUMN_FAMILY: MaxVersionsGCRule(1)})
            table_created = True

        row_key = f"v43::telemetry::{now_iso()}".encode("utf-8")
        row = table.direct_row(row_key)
        row.set_cell(DEFAULT_COLUMN_FAMILY, b"summary", json.dumps(telemetry, sort_keys=True))
        row.set_cell(DEFAULT_COLUMN_FAMILY, b"phase", b"v43_omega")
        row.set_cell(DEFAULT_COLUMN_FAMILY, b"source_prefix", b"v43::telemetry")
        row.commit()

        readback = table.read_row(row_key)
        if readback is None:
            return {
                "state": "blocked_readback_missing",
                "table_created": table_created,
                "row_key": row_key.decode("utf-8"),
                "blocker": "The V43 telemetry row was written but could not be read back.",
            }

        family_cells = getattr(readback, "cells", {}).get(DEFAULT_COLUMN_FAMILY, {})
        summary_cells = family_cells.get(b"summary", [])
        summary_value = summary_cells[0].value.decode("utf-8", errors="replace") if summary_cells else ""
        return {
            "state": "bigtable_v43_prefix_verified" if summary_value else "blocked_readback_missing",
            "table_created": table_created,
            "row_key": row_key.decode("utf-8"),
            "summary_excerpt": summary_value[:2000],
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "state": "blocked_bigtable_exception",
            "blocker": str(exc),
        }


def _provision_project_if_needed(project_id: str, token: str) -> dict[str, Any]:
    url = f"https://discoveryengine.googleapis.com/v1/projects/{project_id}:provision"
    body = {"acceptDataUseTerms": True, "dataUseTermsVersion": "2022-11-23"}
    response = _http_json("POST", url, token, body=body)
    if response["ok"]:
        return {"state": "provisioned_or_already_ready", "response": response}
    return {"state": "provision_attempt_failed", "response": response}


def _ensure_cognitive_datastore(project_id: str, token: str, location: str, datastore_id: str, document_id: str, telemetry: dict[str, Any]) -> dict[str, Any]:
    parent = f"projects/{project_id}/locations/{location}"
    list_url = f"https://discoveryengine.googleapis.com/v1/{parent}/dataStores?pageSize=50"
    listed = _http_json("GET", list_url, token)
    if not listed["ok"] and listed["status_code"] in {400, 403, 404}:
        provision = _provision_project_if_needed(project_id, token)
        listed = _http_json("GET", list_url, token)
    else:
        provision = {"state": "skipped", "response": {}}

    data_store_name = f"{parent}/dataStores/{datastore_id}"
    if listed["ok"]:
        stores = listed["body"].get("dataStores", [])
        if isinstance(stores, list):
            for store in stores:
                if isinstance(store, dict) and str(store.get("name") or "").endswith(f"/{datastore_id}"):
                    create_step = {"state": "reused_existing_datastore", "response": {"body": store, "status_code": listed["status_code"]}}
                    break
            else:
                create_body = {
                    "displayName": "V43 Cognitive Store",
                    "industryVertical": "GENERIC",
                    "contentConfig": "CONTENT_REQUIRED",
                    "solutionTypes": ["SOLUTION_TYPE_SEARCH"],
                }
                create_url = (
                    f"https://discoveryengine.googleapis.com/v1/{parent}/dataStores"
                    f"?dataStoreId={urllib.parse.quote(datastore_id, safe='')}"
                )
                created = _http_json("POST", create_url, token, body=create_body)
                if created["ok"] and created["body"].get("name"):
                    polled = _poll_operation(str(created["body"]["name"]), token)
                    create_step = {"state": "created_datastore", "response": created, "operation": polled}
                else:
                    create_step = {"state": "create_failed", "response": created}
        else:
            create_step = {"state": "list_parse_failed", "response": listed}
    else:
        create_step = {"state": "list_failed", "response": listed}

    get_store = _http_json(
        "GET",
        f"https://discoveryengine.googleapis.com/v1/{data_store_name}",
        token,
    )
    if not get_store["ok"]:
        return {
            "state": "blocked_datastore_unavailable",
            "provision": provision,
            "list": listed,
            "create": create_step,
            "get": get_store,
        }

    document_name = f"{data_store_name}/branches/default_branch/documents/{document_id}"
    get_document = _http_json(
        "GET",
        f"https://discoveryengine.googleapis.com/v1/{document_name}",
        token,
    )
    if not get_document["ok"] and get_document["status_code"] == 404:
        document_body = {
            "id": document_id,
            "structData": {
                "phase": "v43_omega",
                "marker": "V43_COGNITIVE_MARKER",
                "filesystem_promotion_state": str(telemetry.get("filesystem_promotion_state") or ""),
                "wsl_recovery_state": str(telemetry.get("wsl_recovery_state") or ""),
                "google_drive_state": str(telemetry.get("google_drive_state") or ""),
            },
            "content": {
                "mimeType": "text/plain",
                "rawBytes": base64.b64encode(json.dumps(telemetry, sort_keys=True).encode("utf-8")).decode("ascii"),
            },
        }
        create_document = _http_json(
            "POST",
            (
                f"https://discoveryengine.googleapis.com/v1/{data_store_name}/branches/default_branch/documents"
                f"?documentId={urllib.parse.quote(document_id, safe='')}"
            ),
            token,
            body=document_body,
        )
        get_document = _http_json(
            "GET",
            f"https://discoveryengine.googleapis.com/v1/{document_name}",
            token,
        )
    else:
        create_document = {"state": "skipped_existing_document"}

    list_documents = _http_json(
        "GET",
        f"https://discoveryengine.googleapis.com/v1/{data_store_name}/branches/default_branch/documents?pageSize=5",
        token,
    )

    state = "datastore_document_readback_verified" if get_document["ok"] else "blocked_document_readback"
    return {
        "state": state,
        "data_store_name": data_store_name,
        "document_name": document_name,
        "provision": provision,
        "list": listed,
        "create": create_step,
        "get_data_store": get_store,
        "create_document": create_document,
        "get_document": get_document,
        "list_documents": list_documents,
    }


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V43 Vesper Memory And Cognitive Bridge",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Vesper telemetry state: `{payload['vesper_telemetry_ingest_state']}`",
        f"- Vesper cognitive engine state: `{payload['vesper_cognitive_engine_state']}`",
        f"- Bigtable table: `{payload.get('table_id', '')}`",
        f"- Cognitive datastore: `{payload.get('cognitive_data_store_id', '')}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{row}`" for row in payload.get("completed_steps", []))
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write bounded V43 telemetry to Bigtable and prove a minimal cognitive lane.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--instance-id", default=DEFAULT_INSTANCE_ID)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--location", default=DEFAULT_LOCATION)
    parser.add_argument("--data-store-id", default=DEFAULT_DATASTORE_ID)
    parser.add_argument("--document-id", default=DEFAULT_DOCUMENT_ID)
    parser.add_argument("--scheduled", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    bundle_path = Path(args.bundle)
    _records, primary, minted = load_primary_service_account(bundle_path)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "execution_mode": "scheduled" if args.scheduled else "manual",
        "overall_status": "WARN",
        "vesper_telemetry_ingest_state": "pending",
        "vesper_cognitive_engine_state": "pending",
        "project_id": PROJECT_ID,
        "instance_id": args.instance_id,
        "table_id": args.table_id,
        "location": args.location,
        "cognitive_data_store_id": args.data_store_id,
        "cognitive_document_id": args.document_id,
        "completed_steps": [],
        "blockers": [],
        "telemetry": {
            "generated_utc": now_iso(),
            "sources": [_summary(rel_path) for rel_path in TELEMETRY_SOURCES],
        },
    }
    payload.update(primary_identity_fields(primary, minted))
    payload["service_account_path"] = str(primary["runtime_path"])

    bigtable = _ensure_bigtable_table(PROJECT_ID, bundle_path, args.instance_id, args.table_id, payload["telemetry"])
    payload["bigtable_bridge"] = to_jsonable(bigtable)
    payload["vesper_telemetry_ingest_state"] = str(bigtable.get("state") or "blocked")
    if str(bigtable.get("state") or "") == "bigtable_v43_prefix_verified":
        payload["completed_steps"].append("bigtable_write_readback_verified")
    else:
        payload["blockers"].append(str(bigtable.get("blocker") or "Bigtable write/readback did not succeed."))

    telemetry_snapshot = {
        "phase": "v43_omega",
        "marker": "V43_COGNITIVE_MARKER",
        "filesystem_promotion_state": next(
            (
                str(source.get("filesystem_promotion_state") or "")
                for source in payload["telemetry"]["sources"]
                if source.get("filesystem_promotion_state")
            ),
            "",
        ),
        "wsl_recovery_state": next(
            (
                str(source.get("wsl_recovery_state") or "")
                for source in payload["telemetry"]["sources"]
                if source.get("wsl_recovery_state")
            ),
            "",
        ),
        "google_drive_state": next(
            (
                str(source.get("google_drive_state") or "")
                for source in payload["telemetry"]["sources"]
                if source.get("google_drive_state")
            ),
            "",
        ),
    }
    try:
        cognitive = _ensure_cognitive_datastore(PROJECT_ID, minted["token"], args.location, args.data_store_id, args.document_id, telemetry_snapshot)
    except Exception as exc:  # noqa: BLE001
        cognitive = {
            "state": "blocked_cognitive_exception",
            "blocker": str(exc),
        }
    payload["cognitive_engine"] = to_jsonable(cognitive)
    payload["vesper_cognitive_engine_state"] = str(cognitive.get("state") or "blocked")
    if payload["vesper_cognitive_engine_state"] == "datastore_document_readback_verified":
        payload["completed_steps"].append("cognitive_datastore_document_readback_verified")
    else:
        payload["blockers"].append("The bounded Discovery Engine datastore/document proof did not reach a verified readback state.")

    if payload["vesper_telemetry_ingest_state"] == "bigtable_v43_prefix_verified" and payload["vesper_cognitive_engine_state"] == "datastore_document_readback_verified":
        payload["overall_status"] = "PASS"
    elif payload["vesper_telemetry_ingest_state"] == "bigtable_v43_prefix_verified":
        payload["overall_status"] = "WARN"
    else:
        payload["overall_status"] = "FAIL"

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
