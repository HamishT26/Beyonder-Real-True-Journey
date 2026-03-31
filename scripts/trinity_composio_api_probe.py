#!/usr/bin/env python3
"""Run a bounded Composio v3 API verification probe."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILE = Path.home() / ".env file.txt"
OUTPUT_JSON = ROOT / "docs" / "trinity-composio-api-probe-latest.json"
OUTPUT_MD = ROOT / "docs" / "trinity-composio-api-probe-latest.md"
OUTPUT_TRACE = ROOT / "docs" / "trinity-live-traces" / "composio-api-proof-v1.json"
BASE_URL = "https://backend.composio.dev/api/v3"
TOOLKIT_SLUG = "github"
PUBLIC_TOOL_SLUG = "HACKERNEWS_GET_USER"
PUBLIC_TOOL_ARGUMENTS = {"username": "pg"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        parsed = value.strip()
        if len(parsed) >= 2 and ((parsed[0] == parsed[-1] == '"') or (parsed[0] == parsed[-1] == "'")):
            parsed = parsed[1:-1]
        values[key.strip()] = parsed
    return values


def api_key_and_source() -> tuple[str, str]:
    env_key = os.environ.get("COMPOSIO_API_KEY", "").strip()
    if env_key:
        return env_key, "process_env"
    file_values = load_env(DEFAULT_ENV_FILE)
    file_key = file_values.get("COMPOSIO_API_KEY", "").strip()
    if file_key:
        return file_key, str(DEFAULT_ENV_FILE)
    return "", "missing"


def _parse_body(body_text: str) -> Any:
    body = (body_text or "").strip()
    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"raw_body": body}


def request_body(path: str, api_key: str, *, method: str = "GET", json_body: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{BASE_URL}{path}"
    data: bytes | None = None
    headers = {
        "x-api-key": api_key,
        "accept": "application/json",
        "user-agent": "codex-trinity-v29/1.0",
    }
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["content-type"] = "application/json"
    req = urllib.request.Request(
        url,
        headers=headers,
        data=data,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body_text = resp.read().decode("utf-8", errors="replace")
            return {
                "status": resp.status,
                "content_type": resp.headers.get("content-type", ""),
                "body_text": body_text,
                "parsed": _parse_body(body_text),
            }
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        return {
            "status": exc.code,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "body_text": body_text,
            "parsed": _parse_body(body_text),
        }
    except urllib.error.URLError as exc:
        return {
            "status": 0,
            "content_type": "",
            "body_text": "",
            "parsed": {"error": str(exc)},
        }


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _iter_candidate_lists(payload: Any) -> list[list[Any]]:
    lists: list[list[Any]] = []
    if isinstance(payload, list):
        lists.append(payload)
        return lists
    if not isinstance(payload, dict):
        return lists

    for key in ("items", "results", "data", "toolkits", "tools", "accounts", "connected_accounts"):
        value = payload.get(key)
        if isinstance(value, list):
            lists.append(value)
        elif isinstance(value, dict):
            lists.extend(_iter_candidate_lists(value))

    for value in payload.values():
        if isinstance(value, dict):
            lists.extend(_iter_candidate_lists(value))
    return lists


def sample_labels(payload: Any, limit: int = 10) -> list[str]:
    labels: list[str] = []
    seen: set[str] = set()

    def add(candidate: Any) -> None:
        label = _stringify(candidate).strip()
        if not label or label in seen:
            return
        seen.add(label)
        labels.append(label)

    for candidate_list in _iter_candidate_lists(payload):
        for item in candidate_list:
            if len(labels) >= limit:
                return labels
            if isinstance(item, str):
                add(item)
                continue
            if isinstance(item, dict):
                for key in ("slug", "name", "toolkit_slug", "toolkit", "id"):
                    value = item.get(key)
                    if isinstance(value, str) and value:
                        add(value)
                        break
                else:
                    add(item.get("slug") or item.get("name") or item.get("id"))
            else:
                add(item)
    return labels


def first_list_count(payload: Any) -> int | None:
    for candidate_list in _iter_candidate_lists(payload):
        return len(candidate_list)
    return None


def summarize_public_capability(response: dict[str, Any]) -> dict[str, Any]:
    payload = response.get("parsed", {})
    status = int(response.get("status", 0) or 0)
    ok = status == 200
    summary: dict[str, Any] = {
        "tool_slug": PUBLIC_TOOL_SLUG,
        "sample_arguments": {"username": "pg"},
        "status": "PASS" if ok else "FAIL",
        "http_status": status,
        "content_type": response.get("content_type", ""),
        "execution_result_present": False,
        "result_hint": "",
    }
    if isinstance(payload, dict):
        for key in ("successful", "success"):
            if key in payload:
                summary["execution_result_present"] = bool(payload.get(key))
                break
        for key in ("message", "status", "id"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                summary["result_hint"] = value.strip()
                break
        if not summary["result_hint"]:
            data = payload.get("data")
            if isinstance(data, dict):
                for key in ("id", "username", "user", "status"):
                    value = data.get(key)
                    if isinstance(value, str) and value.strip():
                        summary["result_hint"] = value.strip()
                        break
    return summary


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    api_key, key_source = api_key_and_source()
    if not api_key:
        payload = {
            "generated_utc": now_iso(),
            "overall_status": "WARN",
            "proof_state": "missing_api_key",
            "key_source": key_source,
            "verified_composio_toolkits": [],
            "toolkit_visibility_sample": [],
            "connected_account_count": None,
            "http_statuses": {},
            "response_content_types": {},
            "blockers": ["COMPOSIO_API_KEY is missing from process env and the local runtime env file."],
            "notes": [
                "The probe verifies the Composio v3 API directly with x-api-key auth.",
                "verified_composio_toolkits remains empty until a live in-session toolkit surface is actually materialized.",
            ],
        }
        write_json(OUTPUT_JSON, payload)
        write_json(OUTPUT_TRACE, payload)
        write_text(
            OUTPUT_MD,
            "# Trinity Composio API Probe\n\n"
            f"- overall_status: `{payload['overall_status']}`\n"
            f"- proof_state: `{payload['proof_state']}`\n"
            f"- key_source: `{payload['key_source']}`\n"
            "- blockers:\n"
            + "\n".join([f"  - {item}" for item in payload["blockers"]]),
        )
        print(json.dumps({"overall_status": payload["overall_status"], "proof_state": payload["proof_state"]}))
        return 1

    toolkit_response = request_body(f"/toolkits/{TOOLKIT_SLUG}", api_key)
    tools_response = request_body("/tools", api_key)
    accounts_response = request_body("/connected_accounts", api_key)
    public_tool_response = request_body(
        f"/tools/execute/{PUBLIC_TOOL_SLUG}",
        api_key,
        method="POST",
        json_body={"arguments": PUBLIC_TOOL_ARGUMENTS},
    )

    toolkit_status = int(toolkit_response["status"])
    tools_status = int(tools_response["status"])
    accounts_status = int(accounts_response["status"])
    public_tool_status = int(public_tool_response["status"])

    toolkit_payload = toolkit_response["parsed"]
    tools_payload = tools_response["parsed"]
    accounts_payload = accounts_response["parsed"]
    public_capability_probe = summarize_public_capability(public_tool_response)

    toolkit_names = sample_labels(tools_payload, limit=10)
    if not toolkit_names:
        toolkit_names = sample_labels(toolkit_payload, limit=10)

    connected_count = first_list_count(accounts_payload)

    statuses = {toolkit_status, tools_status, accounts_status}
    if 401 in statuses or 403 in statuses:
        proof_state = "invalid_api_key"
        overall_status = "WARN"
    elif toolkit_status == 200 and tools_status == 200 and accounts_status == 200:
        proof_state = "api_verified_connector_unloaded"
        overall_status = "PASS"
    else:
        proof_state = "api_blocked"
        overall_status = "WARN"

    payload = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "proof_state": proof_state,
        "key_source": key_source,
        "verified_composio_toolkits": [],
        "toolkit_visibility_sample": toolkit_names,
        "connected_account_count": connected_count,
        "http_statuses": {
            "toolkit_github": toolkit_status,
            "tools_github": tools_status,
            "connected_accounts": accounts_status,
            "public_tool_execute": public_tool_status,
        },
        "response_content_types": {
            "toolkit_github": toolkit_response.get("content_type", ""),
            "tools_github": tools_response.get("content_type", ""),
            "connected_accounts": accounts_response.get("content_type", ""),
            "public_tool_execute": public_tool_response.get("content_type", ""),
        },
        "public_capability_probe": public_capability_probe,
        "materialized_public_capability_count": 1 if public_capability_probe["status"] == "PASS" else 0,
        "blockers": [],
        "notes": [
            "The probe verifies the Composio v3 API directly with x-api-key auth.",
            "verified_composio_toolkits remains empty until a live in-session toolkit surface is actually materialized.",
        ],
    }

    if proof_state in {"invalid_api_key", "api_blocked"}:
        payload["blockers"] = [
            f"github toolkit probe returned HTTP {toolkit_status}",
            f"github tools probe returned HTTP {tools_status}",
            f"connected_accounts probe returned HTTP {accounts_status}",
        ]
    elif public_capability_probe["status"] == "PASS":
        payload["notes"].append(
            "A safe public tool execution probe succeeded for HACKERNEWS_GET_USER while verified_composio_toolkits remained empty."
        )
    else:
        payload["blockers"] = [
            f"public capability probe for {PUBLIC_TOOL_SLUG} returned HTTP {public_tool_status}",
        ]
        payload["notes"].append(
            "The API surface is verified, but the bounded public tool execution probe did not complete successfully in this run."
        )

    write_json(OUTPUT_JSON, payload)
    write_json(OUTPUT_TRACE, payload)
    write_text(
        OUTPUT_MD,
        "\n".join(
            [
                "# Trinity Composio API Probe",
                "",
                f"- overall_status: `{payload['overall_status']}`",
                f"- proof_state: `{payload['proof_state']}`",
                f"- key_source: `{payload['key_source']}`",
                "",
                "## HTTP Statuses",
                *[
                    f"- {name}: `{status}`"
                    for name, status in payload["http_statuses"].items()
                ],
                "",
                "## Public Capability Probe",
                f"- tool_slug: `{payload['public_capability_probe']['tool_slug']}`",
                f"- status: `{payload['public_capability_probe']['status']}`",
                f"- http_status: `{payload['public_capability_probe']['http_status']}`",
                f"- result_hint: `{payload['public_capability_probe']['result_hint'] or 'n/a'}`",
                "",
                "## Blockers",
                *([f"- {item}" for item in payload["blockers"]] or ["- none"]),
                "",
            ]
        )
        + "\n",
    )
    print(json.dumps({"overall_status": payload["overall_status"], "proof_state": payload["proof_state"]}))
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
