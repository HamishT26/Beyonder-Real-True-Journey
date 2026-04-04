#!/usr/bin/env python3
"""Attempt a real bounded Composio OneDrive materialization lane for V32."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import load_env_values, now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-composio-onedrive-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-composio-onedrive-proof-v1.md"
BASE_URL = "https://backend.composio.dev/api/v3"
KEYWORDS = ("onedrive", "one drive", "microsoft", "office")
SAFE_READ_HINTS = ("list", "search", "get", "folder", "drive")
UNSAFE_HINTS = ("delete", "remove", "upload", "write", "move", "create", "update")
TOOLKIT_CANDIDATES = [
    "onedrive",
    "microsoft_onedrive",
    "microsoft-onedrive",
    "microsoft365",
    "office365",
]


def load_api_key() -> str:
    return load_env_values().get("COMPOSIO_API_KEY", "").strip()


def request_body(path: str, api_key: str, *, method: str = "GET", json_body: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{BASE_URL}{path}"
    data: bytes | None = None
    headers = {
        "x-api-key": api_key,
        "accept": "application/json",
        "user-agent": "codex-trinity-v32/1.0",
    }
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["content-type"] = "application/json"
    request = urllib.request.Request(url, headers=headers, data=data, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body) if body else {}
            except json.JSONDecodeError:
                parsed = {"raw_body": body}
            return {"status": response.status, "parsed": parsed, "body_text": body}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = {"raw_body": body}
        return {"status": exc.code, "parsed": parsed, "body_text": body}
    except urllib.error.URLError as exc:
        return {"status": 0, "parsed": {"error": str(exc)}, "body_text": ""}


def candidate_lists(payload: Any) -> list[list[Any]]:
    if isinstance(payload, list):
        return [payload]
    if not isinstance(payload, dict):
        return []
    results: list[list[Any]] = []
    for key in ("items", "results", "data", "toolkits", "tools", "accounts", "connected_accounts"):
        value = payload.get(key)
        if isinstance(value, list):
            results.append(value)
        elif isinstance(value, dict):
            results.extend(candidate_lists(value))
    for value in payload.values():
        if isinstance(value, dict):
            results.extend(candidate_lists(value))
    return results


def flatten_items(payload: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in candidate_lists(payload):
        for item in group:
            if isinstance(item, dict):
                rows.append(item)
    return rows


def contains_keyword(value: str) -> bool:
    lowered = value.lower()
    return any(keyword in lowered for keyword in KEYWORDS)


def record_matches(record: dict[str, Any]) -> bool:
    fields = [
        str(record.get("slug", "")),
        str(record.get("name", "")),
        str(record.get("toolkit", "")),
        str(record.get("toolkit_slug", "")),
        str(record.get("provider", "")),
        str(record.get("appName", "")),
        str(record.get("displayName", "")),
    ]
    return contains_keyword(" ".join(fields))


def select_safe_tool(tools: list[dict[str, Any]]) -> dict[str, Any] | None:
    for tool in tools:
        slug = str(tool.get("slug") or tool.get("name") or "")
        lowered = slug.lower()
        if any(marker in lowered for marker in UNSAFE_HINTS):
            continue
        if any(marker in lowered for marker in SAFE_READ_HINTS):
            return tool
    return tools[0] if tools else None


def execute_candidates(api_key: str, tool_slug: str, account_id: str) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for body in (
        {"arguments": {}, "connectedAccountId": account_id},
        {"arguments": {}, "connected_account_id": account_id},
        {"arguments": {}, "connectionId": account_id},
        {"arguments": {}, "connectedAccount": account_id},
    ):
        response = request_body(f"/tools/execute/{tool_slug}", api_key, method="POST", json_body=body)
        attempts.append({"request_body": body, "status": response["status"], "parsed": response.get("parsed", {})})
        if response["status"] == 200:
            break
    return attempts


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 Composio OneDrive Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Connected account count: `{payload.get('connected_account_count', 'unknown')}`",
        "",
        "## Notes",
        "",
    ]
    for note in payload.get("notes", []):
        lines.append(f"- {note}")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    api_key = load_api_key()
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "WARN",
        "proof_state": "pending",
        "verified_composio_toolkits": [],
        "connected_account_count": 0,
        "toolkit_candidates": TOOLKIT_CANDIDATES,
        "notes": [
            "V32 attempts a bounded OneDrive-connected toolkit materialization instead of reusing the generic GitHub/public-capability probe.",
            "Only safe read-style tool candidates are considered for execution attempts.",
        ],
        "blockers": [],
    }
    if not api_key:
        payload["proof_state"] = "missing_api_key"
        payload["blockers"].append("COMPOSIO_API_KEY is missing from the local environment.")
        write_outputs(payload)
        return 1

    toolkit_responses = {slug: request_body(f"/toolkits/{slug}", api_key) for slug in TOOLKIT_CANDIDATES}
    tools_response = request_body("/tools", api_key)
    accounts_response = request_body("/connected_accounts", api_key)
    payload["http_statuses"] = {
        **{f"toolkit_{slug}": response["status"] for slug, response in toolkit_responses.items()},
        "tools": tools_response["status"],
        "connected_accounts": accounts_response["status"],
    }

    visible_toolkits = [slug for slug, response in toolkit_responses.items() if response["status"] == 200]
    all_tools = flatten_items(tools_response.get("parsed", {}))
    onedrive_tools = [tool for tool in all_tools if record_matches(tool)]
    all_accounts = flatten_items(accounts_response.get("parsed", {}))
    onedrive_accounts = [account for account in all_accounts if record_matches(account)]

    payload["visible_toolkits"] = visible_toolkits
    payload["connected_account_count"] = len(all_accounts)
    payload["onedrive_connected_account_count"] = len(onedrive_accounts)
    payload["onedrive_tool_sample"] = [
        str(tool.get("slug") or tool.get("name") or "") for tool in onedrive_tools[:10]
    ]

    if not visible_toolkits and not onedrive_tools:
        payload["proof_state"] = "onedrive_toolkit_not_visible"
        payload["blockers"].append("No OneDrive-leaning toolkit or tool surface was visible through the Composio v3 API.")
        write_outputs(payload)
        return 1

    if not onedrive_accounts:
        payload["proof_state"] = "onedrive_connected_account_not_visible"
        payload["blockers"].append("The Composio API did not expose a connected OneDrive account in-session.")
        write_outputs(payload)
        return 1

    safe_tool = select_safe_tool(onedrive_tools)
    if safe_tool is None:
        payload["proof_state"] = "onedrive_no_safe_read_tool"
        payload["blockers"].append("A OneDrive-connected account was visible, but no safe read-style tool candidate was found.")
        write_outputs(payload)
        return 1

    account = onedrive_accounts[0]
    account_id = str(
        account.get("id")
        or account.get("connectedAccountId")
        or account.get("connected_account_id")
        or account.get("connectionId")
        or ""
    )
    tool_slug = str(safe_tool.get("slug") or safe_tool.get("name") or "")
    payload["attempted_tool_slug"] = tool_slug
    payload["attempted_account_reference"] = account_id or "missing_id"

    if not account_id or not tool_slug:
        payload["proof_state"] = "onedrive_execute_reference_missing"
        payload["blockers"].append("Tool or account metadata was visible, but a usable execution reference could not be derived.")
        write_outputs(payload)
        return 1

    attempts = execute_candidates(api_key, tool_slug, account_id)
    payload["execution_attempts"] = attempts
    success = next((row for row in attempts if row["status"] == 200), None)
    if success:
        payload["overall_status"] = "PASS"
        payload["proof_state"] = "toolkit_materialized_connected_read"
        payload["verified_composio_toolkits"] = ["onedrive"]
        payload["execution_result"] = success["parsed"]
        write_outputs(payload)
        return 0

    payload["proof_state"] = "toolkit_visible_but_execute_blocked"
    payload["blockers"].append(
        "OneDrive toolkit visibility and connected-account discovery succeeded, but the bounded read execution attempt did not complete."
    )
    write_outputs(payload)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
