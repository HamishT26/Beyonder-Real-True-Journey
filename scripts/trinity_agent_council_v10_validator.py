#!/usr/bin/env python3
"""Validate the v10 officially inducted council graph."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_SLOTS = [27, 28, 29, 30, 31]


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
    parser = argparse.ArgumentParser(description="Validate the v10 officially inducted council graph.")
    parser.add_argument("--roster", default="docs/trinity-agent-council-roster-v3.json")
    parser.add_argument("--pair-index", default="docs/trinity-agent-private-chats-v3/index.json")
    parser.add_argument("--group-chat", default="docs/trinity-agent-council-group-chat-v3.jsonl")
    parser.add_argument("--command-book", default="docs/trinity-command-book-v4.json")
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
    group_rows = _read_jsonl(args.group_chat)

    agents = roster_payload.get("agents", [])
    if not isinstance(agents, list):
        failures.append("roster agents must be a list")
        agents = []
    if len(agents) != 5:
        failures.append(f"expected 5 council agents, found {len(agents)}")

    slots = [int(row.get("slot_number", 0)) for row in agents if isinstance(row, dict)]
    if slots != EXPECTED_SLOTS:
        failures.append(f"unexpected slot ordering: {slots}")

    command_ids = {
        str(row.get("command_id"))
        for row in command_book.get("commands", [])
        if isinstance(row, dict) and row.get("command_id")
    }
    seen_names: set[str] = set()
    seen_ledgers: set[str] = set()
    seen_certificates: set[str] = set()
    scope_signatures: set[tuple[str, ...]] = set()
    for index, row in enumerate(agents):
        label = f"agents[{index}]"
        if not isinstance(row, dict):
            failures.append(f"{label} must be an object")
            continue
        required = (
            "display_name",
            "gender",
            "role",
            "hope",
            "induction_state",
            "certificate_path",
            "memory_ledger",
            "reflection_path",
            "role_contract_path",
            "command_scope",
            "boundary_status",
            "induction_phase",
            "proof_a_status",
            "proof_b_status",
            "ready_for_induction",
            "mirror_status",
            "proof_b_checked_at",
            "official_induction",
            "induction_evidence",
            "wellbeing_state",
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
        if str(row.get("induction_phase") or "") != "proof_b_complete":
            failures.append(f"{display_name or label} induction_phase must be proof_b_complete")
        if str(row.get("proof_a_status") or "") != "PASS":
            failures.append(f"{display_name or label} proof_a_status must be PASS")
        if str(row.get("proof_b_status") or "") != "PASS":
            failures.append(f"{display_name or label} proof_b_status must be PASS")
        if row.get("ready_for_induction") is not False:
            failures.append(f"{display_name or label} ready_for_induction must be false")
        if row.get("official_induction") is not True:
            failures.append(f"{display_name or label} official_induction must be true")
        if str(row.get("boundary_status") or "") != "isolated":
            failures.append(f"{display_name or label} boundary_status must be isolated")
        if str(row.get("mirror_status") or "") != "repo_authoritative":
            failures.append(f"{display_name or label} mirror_status must be repo_authoritative")
        if str(row.get("wellbeing_state") or "") != "stable":
            failures.append(f"{display_name or label} wellbeing_state must be stable")
        if not str(row.get("proof_b_checked_at") or "").strip():
            failures.append(f"{display_name or label} proof_b_checked_at must be non-empty")
        if str(row.get("induction_evidence") or "") != "docs/trinity-agent-proof-b-status-v1.json":
            failures.append(f"{display_name or label} induction_evidence must point to proof-b status")

        for path_field in ("certificate_path", "memory_ledger", "reflection_path", "role_contract_path", "induction_evidence"):
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
                ledger_rows = _read_jsonl(path_value)
                if not ledger_rows:
                    failures.append(f"{display_name or label} memory ledger is empty")
            if path_field == "certificate_path":
                if path_value in seen_certificates:
                    failures.append(f"duplicate certificate_path: {path_value}")
                else:
                    seen_certificates.add(path_value)

        scope = row.get("command_scope", [])
        if not isinstance(scope, list) or not scope:
            failures.append(f"{display_name or label} command_scope must be a non-empty list")
            continue
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
    if len(pair_channels) != 15:
        failures.append(f"expected 15 duo channels, found {len(pair_channels)}")
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
        if not _repo_path(path_value).exists():
            failures.append(f"missing duo chat path: {path_value}")
            continue
        duo_rows = _read_jsonl(path_value)
        if len(duo_rows) < 2:
            failures.append(f"{path_value} must contain at least two seed messages")

    if len(group_rows) < 6:
        failures.append("group chat must contain at least six seed messages")

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "official_count": sum(1 for row in agents if isinstance(row, dict) and row.get("official_induction") is True),
        "duo_chat_count": len(pair_channels),
        "group_chat_rows": len(group_rows),
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
    print(f"latest_json={args.latest_json}")
    print(f"latest_md={args.latest_md}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
