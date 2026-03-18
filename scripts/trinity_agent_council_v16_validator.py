#!/usr/bin/env python3
"""Validate the v16 council mesh, Codex agent definitions, and proof graph."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_SLOTS = list(range(27, 38))
EXPECTED_PAIR_COUNT = ((len(EXPECTED_SLOTS) + 1) * len(EXPECTED_SLOTS)) // 2
EXPECTED_AGENT_COUNT = len(EXPECTED_SLOTS)
EXPECTED_REQUESTED_MODEL = "gpt-5.4"
EXPECTED_RESOLVED_MODEL = "gpt-5.1-codex-max"
EXPECTED_REASONING = "high"
EXPECTED_MAX_THREADS = 11


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path_str: str) -> dict[str, Any]:
    return json.loads(_repo_path(path_str).read_text(encoding="utf-8"))


def _read_jsonl(path_str: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(_repo_path(path_str).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"{path_str} line {index} must decode to an object")
        rows.append(payload)
    return rows


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Trinity Agent Council Validation",
            "",
            f"- generated_utc: `{payload['generated_utc']}`",
            f"- overall_status: **{payload['overall_status']}**",
            f"- official_count: `{payload['official_count']}`",
            f"- duo_chat_count: `{payload['duo_chat_count']}`",
            f"- group_chat_rows: `{payload['group_chat_rows']}`",
            f"- requested_model_profile: `{payload['requested_model_profile']}`",
            f"- resolved_model_profile: `{payload['resolved_model_profile']}`",
            f"- max_threads: `{payload['max_threads']}`",
            "",
            "## Failures",
            *([f"- {item}" for item in payload["failures"]] or ["- none"]),
            "",
            "## Warnings",
            *([f"- {item}" for item in payload["warnings"]] or ["- none"]),
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the v16 council mesh and Codex agent graph.")
    parser.add_argument("--roster", default="docs/trinity-agent-council-roster-v6.json")
    parser.add_argument("--pair-index", default="docs/trinity-agent-private-chats-v5/index.json")
    parser.add_argument("--group-chat", default="docs/trinity-agent-council-group-chat-v5.jsonl")
    parser.add_argument("--command-book", default="docs/trinity-command-book-v10.json")
    parser.add_argument("--subagent-registry", default="docs/trinity-subagent-registry-v3.json")
    parser.add_argument("--proof-json", default="docs/trinity-agent-mesh-proof-v1.json")
    parser.add_argument("--codex-config", default=".codex/config.toml")
    parser.add_argument("--reports-dir", default="docs/trinity-agent-council-runs")
    parser.add_argument("--latest-json", default="docs/trinity-agent-council-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-agent-council-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    roster_payload = _read_json(args.roster)
    pair_payload = _read_json(args.pair_index)
    command_book = _read_json(args.command_book)
    subagent_registry = _read_json(args.subagent_registry)
    proof_payload = _read_json(args.proof_json)
    group_rows = _read_jsonl(args.group_chat)

    codex_config_path = _repo_path(args.codex_config)
    if not codex_config_path.exists():
        failures.append(f"missing codex config: {args.codex_config}")
        codex_config_text = ""
    else:
        codex_config_text = codex_config_path.read_text(encoding="utf-8")

    if f"max_threads = {EXPECTED_MAX_THREADS}" not in codex_config_text:
        failures.append(f"codex config must set max_threads = {EXPECTED_MAX_THREADS}")
    if f'requested_model_profile = "{EXPECTED_REQUESTED_MODEL}"' not in codex_config_text:
        failures.append(f"codex config must request {EXPECTED_REQUESTED_MODEL}")
    if f'resolved_model_profile = "{EXPECTED_RESOLVED_MODEL}"' not in codex_config_text:
        failures.append(f"codex config must resolve {EXPECTED_RESOLVED_MODEL}")
    if f'resolved_reasoning_effort = "{EXPECTED_REASONING}"' not in codex_config_text:
        failures.append(f"codex config must resolve reasoning {EXPECTED_REASONING}")

    agents = roster_payload.get("agents", [])
    if not isinstance(agents, list):
        failures.append("roster agents must be a list")
        agents = []
    if len(agents) != EXPECTED_AGENT_COUNT:
        failures.append(f"expected {EXPECTED_AGENT_COUNT} council agents, found {len(agents)}")

    slots = [int(row.get("slot_number", 0)) for row in agents if isinstance(row, dict)]
    if slots != EXPECTED_SLOTS:
        failures.append(f"unexpected slot ordering: {slots}")

    requested_model_profile = str(roster_payload.get("requested_model_profile") or "")
    resolved_model_profile = str(roster_payload.get("resolved_model_profile") or "")
    max_threads = int(roster_payload.get("max_threads", 0) or 0)
    if requested_model_profile != EXPECTED_REQUESTED_MODEL:
        failures.append(f"roster requested_model_profile must be {EXPECTED_REQUESTED_MODEL}")
    if resolved_model_profile != EXPECTED_RESOLVED_MODEL:
        failures.append(f"roster resolved_model_profile must be {EXPECTED_RESOLVED_MODEL}")
    if max_threads != EXPECTED_MAX_THREADS:
        failures.append(f"roster max_threads must be {EXPECTED_MAX_THREADS}")

    command_ids = {
        str(row.get("command_id"))
        for row in command_book.get("commands", [])
        if isinstance(row, dict) and row.get("command_id")
    }
    seen_names: set[str] = set()
    seen_ledgers: set[str] = set()
    seen_certificates: set[str] = set()
    seen_codex_ids: set[str] = set()
    seen_codex_paths: set[str] = set()
    scope_signatures: set[tuple[str, ...]] = set()

    for index, row in enumerate(agents):
        label = f"agents[{index}]"
        if not isinstance(row, dict):
            failures.append(f"{label} must be an object")
            continue
        required = (
            "display_name",
            "role",
            "induction_state",
            "certificate_path",
            "memory_ledger",
            "reflection_path",
            "role_contract_path",
            "command_scope",
            "boundary_status",
            "proof_a_status",
            "proof_b_status",
            "mirror_status",
            "official_induction",
            "wellbeing_state",
            "agent_class",
            "app_adapter_status",
            "official_after_proof",
            "codex_agent_id",
            "codex_agent_path",
            "mesh_state",
            "requested_model_profile",
            "resolved_model_profile",
            "requested_reasoning_effort",
            "resolved_reasoning_effort",
            "chat_window_binding",
        )
        for field in required:
            if field not in row:
                failures.append(f"{label} missing field: {field}")

        display_name = str(row.get("display_name") or "")
        if not display_name:
            failures.append(f"{label} missing display_name")
        elif display_name in seen_names:
            failures.append(f"duplicate display_name: {display_name}")
        else:
            seen_names.add(display_name)

        if str(row.get("induction_state") or "") != "official":
            failures.append(f"{display_name or label} induction_state must be official")
        if str(row.get("proof_a_status") or "") != "PASS":
            failures.append(f"{display_name or label} proof_a_status must be PASS")
        if str(row.get("proof_b_status") or "") != "PASS":
            failures.append(f"{display_name or label} proof_b_status must be PASS")
        if row.get("official_induction") is not True:
            failures.append(f"{display_name or label} official_induction must be true")
        if str(row.get("boundary_status") or "") != "isolated":
            failures.append(f"{display_name or label} boundary_status must be isolated")
        if str(row.get("mirror_status") or "") != "repo_authoritative":
            failures.append(f"{display_name or label} mirror_status must be repo_authoritative")
        if str(row.get("wellbeing_state") or "") != "stable":
            failures.append(f"{display_name or label} wellbeing_state must be stable")
        if str(row.get("mesh_state") or "") != "active_project_custom_agent":
            failures.append(f"{display_name or label} mesh_state must be active_project_custom_agent")
        if str(row.get("requested_model_profile") or "") != EXPECTED_REQUESTED_MODEL:
            failures.append(f"{display_name or label} requested_model_profile must be {EXPECTED_REQUESTED_MODEL}")
        if str(row.get("resolved_model_profile") or "") != EXPECTED_RESOLVED_MODEL:
            failures.append(f"{display_name or label} resolved_model_profile must be {EXPECTED_RESOLVED_MODEL}")
        if str(row.get("requested_reasoning_effort") or "") != EXPECTED_REASONING:
            failures.append(f"{display_name or label} requested_reasoning_effort must be {EXPECTED_REASONING}")
        if str(row.get("resolved_reasoning_effort") or "") != EXPECTED_REASONING:
            failures.append(f"{display_name or label} resolved_reasoning_effort must be {EXPECTED_REASONING}")
        if not str(row.get("chat_window_binding") or "").strip():
            failures.append(f"{display_name or label} chat_window_binding must be non-empty")

        codex_agent_id = str(row.get("codex_agent_id") or "")
        codex_agent_path = str(row.get("codex_agent_path") or "")
        if not codex_agent_id:
            failures.append(f"{display_name or label} missing codex_agent_id")
        elif codex_agent_id in seen_codex_ids:
            failures.append(f"duplicate codex_agent_id: {codex_agent_id}")
        else:
            seen_codex_ids.add(codex_agent_id)
        if not codex_agent_path:
            failures.append(f"{display_name or label} missing codex_agent_path")
        elif codex_agent_path in seen_codex_paths:
            failures.append(f"duplicate codex_agent_path: {codex_agent_path}")
        else:
            seen_codex_paths.add(codex_agent_path)
            codex_path = _repo_path(codex_agent_path)
            if not codex_path.exists():
                failures.append(f"{display_name or label} missing codex agent file: {codex_agent_path}")
            else:
                codex_text = codex_path.read_text(encoding="utf-8")
                if f'name: "{display_name}"' not in codex_text:
                    failures.append(f"{display_name or label} codex agent file missing name header")
                if EXPECTED_RESOLVED_MODEL not in codex_text:
                    failures.append(f"{display_name or label} codex agent file missing resolved model")

        for path_field in ("certificate_path", "memory_ledger", "reflection_path", "role_contract_path"):
            path_value = str(row.get(path_field) or "")
            if not path_value:
                failures.append(f"{display_name or label} missing {path_field}")
                continue
            path = _repo_path(path_value)
            if not path.exists():
                failures.append(f"{display_name or label} missing path: {path_value}")
            if path_field == "memory_ledger":
                if path_value in seen_ledgers:
                    failures.append(f"duplicate memory_ledger: {path_value}")
                else:
                    seen_ledgers.add(path_value)
            if path_field == "certificate_path":
                if path_value in seen_certificates:
                    failures.append(f"duplicate certificate_path: {path_value}")
                else:
                    seen_certificates.add(path_value)

        scope = row.get("command_scope", [])
        if not isinstance(scope, list) or not scope:
            failures.append(f"{display_name or label} command_scope must be a non-empty list")
        else:
            invalid_scope = [item for item in scope if str(item) not in command_ids]
            if invalid_scope:
                failures.append(f"{display_name or label} command_scope references unknown commands: {invalid_scope}")
            signature = tuple(sorted(str(item) for item in scope))
            if signature in scope_signatures:
                failures.append(f"{display_name or label} shares an identical command scope with another agent")
            else:
                scope_signatures.add(signature)

    pair_channels = pair_payload.get("pair_channels", [])
    if not isinstance(pair_channels, list):
        failures.append("pair_channels must be a list")
        pair_channels = []
    if len(pair_channels) != EXPECTED_PAIR_COUNT:
        failures.append(f"expected {EXPECTED_PAIR_COUNT} duo channels, found {len(pair_channels)}")
    for index, row in enumerate(pair_channels):
        if not isinstance(row, dict):
            failures.append(f"pair_channels[{index}] must be an object")
            continue
        if str(row.get("privacy_class") or "") != "private_duo":
            failures.append(f"pair_channels[{index}] must have privacy_class=private_duo")
        path_value = str(row.get("path") or "")
        if not path_value:
            failures.append(f"pair_channels[{index}] missing path")
            continue
        duo_path = _repo_path(path_value)
        if not duo_path.exists():
            failures.append(f"missing duo chat path: {path_value}")
            continue
        duo_rows = _read_jsonl(path_value)
        if len(duo_rows) < 2:
            failures.append(f"{path_value} must contain at least two seed messages")

    if len(group_rows) < EXPECTED_AGENT_COUNT + 1:
        failures.append(f"group chat must contain at least {EXPECTED_AGENT_COUNT + 1} seed messages")

    subagents = subagent_registry.get("subagents", [])
    if not isinstance(subagents, list) or len(subagents) != EXPECTED_AGENT_COUNT:
        failures.append(f"subagent registry must contain exactly {EXPECTED_AGENT_COUNT} entries")
        subagents = []
    for row in subagents:
        if not isinstance(row, dict):
            failures.append("subagent registry entries must be objects")
            continue
        slot_number = int(row.get("slot_number", 0) or 0)
        if slot_number not in EXPECTED_SLOTS:
            failures.append(f"unexpected subagent slot: {row.get('slot_number')}")
        if str(row.get("proof_state") or "") != "PASS":
            failures.append(f"subagent {row.get('display_name')} proof_state must be PASS")
        if str(row.get("requested_model_profile") or "") != EXPECTED_REQUESTED_MODEL:
            failures.append(f"subagent {row.get('display_name')} requested_model_profile must be {EXPECTED_REQUESTED_MODEL}")
        if str(row.get("resolved_model_profile") or "") != EXPECTED_RESOLVED_MODEL:
            failures.append(f"subagent {row.get('display_name')} resolved_model_profile must be {EXPECTED_RESOLVED_MODEL}")
        if str(row.get("resolved_reasoning_effort") or "") != EXPECTED_REASONING:
            failures.append(f"subagent {row.get('display_name')} resolved_reasoning_effort must be {EXPECTED_REASONING}")

    if str(proof_payload.get("overall_status") or "") != "PASS":
        failures.append("mesh proof artifact must be PASS")
    if int(proof_payload.get("official_agent_count", 0) or 0) != EXPECTED_AGENT_COUNT:
        failures.append(f"mesh proof official_agent_count must be {EXPECTED_AGENT_COUNT}")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "official_count": sum(1 for row in agents if isinstance(row, dict) and row.get("official_induction") is True),
        "provisional_agent_count": 0,
        "duo_chat_count": len(pair_channels),
        "group_chat_rows": len(group_rows),
        "requested_model_profile": requested_model_profile or EXPECTED_REQUESTED_MODEL,
        "resolved_model_profile": resolved_model_profile or EXPECTED_RESOLVED_MODEL,
        "max_threads": max_threads or EXPECTED_MAX_THREADS,
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }
    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (reports_dir / f"{stamp}-trinity-agent-council-validation.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (reports_dir / f"{stamp}-trinity-agent-council-validation.md").write_text(_markdown(payload), encoding="utf-8")
    _repo_path(args.latest_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _repo_path(args.latest_md).write_text(_markdown(payload), encoding="utf-8")
    print(f"overall_status={payload['overall_status']}")
    print(f"effective_success={payload['effective_success']}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
