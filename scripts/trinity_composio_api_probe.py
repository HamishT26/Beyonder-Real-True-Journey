#!/usr/bin/env python3
"""Run a bounded Composio v3 API verification probe."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
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
    env_file = DEFAULT_ENV_FILE
    file_values = load_env(env_file)
    file_key = file_values.get("COMPOSIO_API_KEY", "").strip()
    if file_key:
        return file_key, str(env_file)
    return "", "missing"


def request_json(path: str, api_key: str) -> tuple[int, Any]:
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "x-api-key": api_key,
            "accept": "application/json",
            "user-agent": "codex-trinity-v27/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = {"raw_body": body}
        return exc.code, payload


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

    toolkit_status, toolkit_payload = request_json("/toolkits/github", api_key)
    tools_status, tools_payload = request_json("/tools?" + urllib.parse.urlencode({"toolkit": "github", "limit": 10}), api_key)
    accounts_status, accounts_payload = request_json("/connectedAccounts?" + urllib.parse.urlencode({"limit": 10}), api_key)

    toolkit_names: list[str] = []
    if isinstance(tools_payload, dict):
        items = tools_payload.get("items") or tools_payload.get("results") or []
        if isinstance(items, list):
            for item in items[:10]:
                if isinstance(item, dict):
                    name = item.get("slug") or item.get("name")
                    if isinstance(name, str) and name:
                        toolkit_names.append(name)

    connected_count = None
    if isinstance(accounts_payload, dict):
        items = accounts_payload.get("items") or accounts_payload.get("results")
        if isinstance(items, list):
            connected_count = len(items)

    if 401 in {toolkit_status, tools_status, accounts_status}:
        proof_state = "invalid_api_key"
        overall_status = "WARN"
    elif toolkit_status == 200 and tools_status == 200:
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
        },
        "blockers": [],
        "notes": [
            "The probe verifies the Composio v3 API directly with x-api-key auth.",
            "verified_composio_toolkits remains empty until a live in-session toolkit surface is actually materialized.",
        ],
    }

    if proof_state == "invalid_api_key":
        payload["blockers"] = [
            f"github toolkit probe returned HTTP {toolkit_status}",
            f"github tools probe returned HTTP {tools_status}",
            f"connected_accounts probe returned HTTP {accounts_status}",
        ]
    elif proof_state == "api_blocked":
        payload["blockers"] = [
            f"github toolkit probe returned HTTP {toolkit_status}",
            f"github tools probe returned HTTP {tools_status}",
            f"connected_accounts probe returned HTTP {accounts_status}",
        ]

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
