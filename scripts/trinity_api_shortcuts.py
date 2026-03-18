#!/usr/bin/env python3
"""Operator-friendly shortcuts for the governed Trinity API book."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_BOOK_PATH = ROOT / "docs" / "trinity-api-book-v5.json"
MEMORY_BANK_PATH = ROOT / "docs" / "trinity-memory-bank-registry-v3.json"
PUBLIC_SIGNAL_PATH = ROOT / "docs" / "trinity-public-signal-board-latest.json"
PUBLIC_VALIDATION_PATH = ROOT / "docs" / "trinity-public-research-validation-latest.json"
CONTROL_TOWER_PATH = ROOT / "docs" / "trinity-control-tower-latest.json"
COUNCIL_ROSTER_PATH = ROOT / "docs" / "trinity-agent-council-roster-v6.json"
SUBAGENT_REGISTRY_PATH = ROOT / "docs" / "trinity-subagent-registry-v3.json"
INSTANCE_REGISTRY_PATH = ROOT / "docs" / "trinity-instance-registry-v1.json"
CODEX_ADAPTER_PATH = ROOT / "docs" / "trinity-codex-subagent-adapter-v1.json"
AGENT_MESH_PATH = ROOT / "docs" / "trinity-codex-agent-mesh-v1.json"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_api_rows() -> list[dict[str, object]]:
    payload = load_json(API_BOOK_PATH)
    rows = payload.get("apis", [])
    return [row for row in rows if isinstance(row, dict)]


def find_api(api_id: str) -> dict[str, object]:
    for row in load_api_rows():
        if str(row.get("api_id") or "").strip() == api_id:
            return row
    raise SystemExit(f"unknown api_id: {api_id}")


def run_capture(args: list[str], timeout: int = 20) -> dict[str, object]:
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "returncode": 124,
            "stdout": "",
            "stderr": f"command timed out after {timeout} seconds",
        }
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def print_json(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2))


def cmd_list(args: argparse.Namespace) -> int:
    rows = load_api_rows()
    if args.json:
        print_json({"api_count": len(rows), "apis": rows})
        return 0
    for row in rows:
        print(f"{row['api_id']}: {row['surface']} [{row['trust_class']}]")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    row = find_api(args.api_id)
    if args.json:
        print_json(row)
        return 0
    print(json.dumps(row, indent=2))
    return 0


def cmd_memory_bank_status(args: argparse.Namespace) -> int:
    payload = load_json(MEMORY_BANK_PATH)
    summary = {
        "overall_status": payload.get("overall_status"),
        "storage_pressure_class": payload.get("storage_pressure_class"),
        "free_gib": payload.get("storage_pressure", {}).get("free_gib") if isinstance(payload.get("storage_pressure"), dict) else None,
        "retained_snapshot_count": payload.get("retained_snapshot_count"),
        "surfaces": [
            {
                "surface": row.get("surface"),
                "status": row.get("status"),
                "reachable": row.get("reachable"),
                "proof_state": row.get("proof_state"),
            }
            for row in payload.get("memory_banks", [])
            if isinstance(row, dict)
        ],
    }
    if args.json:
        print_json(summary)
    else:
        print(json.dumps(summary, indent=2))
    return 0


def cmd_public_research_status(args: argparse.Namespace) -> int:
    validation = load_json(PUBLIC_VALIDATION_PATH)
    signal = load_json(PUBLIC_SIGNAL_PATH)
    summary = {
        "validation_status": validation.get("overall_status"),
        "signal_status": signal.get("overall_status"),
        "source_count": signal.get("source_count"),
        "freshness_status": signal.get("freshness_status"),
    }
    if args.json:
        print_json(summary)
    else:
        print(json.dumps(summary, indent=2))
    return 0


def cmd_control_tower_status(args: argparse.Namespace) -> int:
    payload = load_json(CONTROL_TOWER_PATH)
    if args.json:
        print_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0


def cmd_council_roster_status(args: argparse.Namespace) -> int:
    payload = load_json(COUNCIL_ROSTER_PATH)
    agents = [row for row in payload.get("agents", []) if isinstance(row, dict)]
    summary = {
        "generated_utc": payload.get("generated_utc"),
        "official_agent_count": len(agents),
        "agents": [
            {
                "slot_number": row.get("slot_number"),
                "display_name": row.get("display_name"),
                "role": row.get("role"),
                "agent_class": row.get("agent_class"),
                "official_after_proof": row.get("official_after_proof"),
            }
            for row in agents
        ],
    }
    if args.json:
        print_json(summary)
    else:
        print(json.dumps(summary, indent=2))
    return 0


def cmd_subagent_status(args: argparse.Namespace) -> int:
    payload = load_json(SUBAGENT_REGISTRY_PATH)
    if args.json:
        print_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0


def cmd_multi_instance_status(args: argparse.Namespace) -> int:
    payload = load_json(INSTANCE_REGISTRY_PATH)
    if args.json:
        print_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0


def cmd_codex_adapter_status(args: argparse.Namespace) -> int:
    payload = load_json(CODEX_ADAPTER_PATH)
    if args.json:
        print_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0


def cmd_agent_mesh_status(args: argparse.Namespace) -> int:
    payload = load_json(AGENT_MESH_PATH)
    if args.json:
        print_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0


def cmd_github_status(args: argparse.Namespace) -> int:
    branch = run_capture(["git", "branch", "--show-current"])
    remote = run_capture(["git", "ls-remote", "origin", "HEAD"], timeout=30)
    payload = {
        "current_branch": branch.get("stdout") or "unknown",
        "remote_reachable": bool(remote.get("ok") and remote.get("stdout")),
        "remote_head": (remote.get("stdout") or "").split()[0] if remote.get("stdout") else "",
        "stderr": remote.get("stderr") or "",
    }
    if args.json:
        print_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0 if payload["remote_reachable"] else 1


def cmd_docker_status(args: argparse.Namespace) -> int:
    payload = run_capture(["docker", "ps", "--format", "{{.Names}}\t{{.Status}}\t{{.Image}}"], timeout=30)
    rows = []
    for line in str(payload.get("stdout") or "").splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            rows.append({"name": parts[0], "status": parts[1], "image": parts[2]})
    result = {
        "docker_available": bool(payload.get("ok")),
        "containers": rows,
        "stderr": payload.get("stderr") or "",
    }
    if args.json:
        print_json(result)
    else:
        print(json.dumps(result, indent=2))
    return 0 if result["docker_available"] else 1


def cmd_postgres_status(args: argparse.Namespace) -> int:
    result = run_capture(
        ["docker", "exec", "trinity-v5-pg-proof", "pg_isready", "-U", "postgres"],
        timeout=20,
    )
    payload = {
        "postgres_ready": bool(result.get("ok")),
        "stdout": result.get("stdout") or "",
        "stderr": result.get("stderr") or "",
    }
    if args.json:
        print_json(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0 if payload["postgres_ready"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Shortcuts for the governed Trinity API book.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List all governed API surfaces.")
    list_parser.add_argument("--json", action="store_true")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="Show one governed API surface entry.")
    show_parser.add_argument("api_id")
    show_parser.add_argument("--json", action="store_true")
    show_parser.set_defaults(func=cmd_show)

    memory_parser = subparsers.add_parser("memory-bank-status", help="Summarize current memory-bank posture.")
    memory_parser.add_argument("--json", action="store_true")
    memory_parser.set_defaults(func=cmd_memory_bank_status)

    public_parser = subparsers.add_parser("public-research-status", help="Summarize public research validation posture.")
    public_parser.add_argument("--json", action="store_true")
    public_parser.set_defaults(func=cmd_public_research_status)

    control_tower_parser = subparsers.add_parser("control-tower-status", help="Summarize the current Trinity control tower.")
    control_tower_parser.add_argument("--json", action="store_true")
    control_tower_parser.set_defaults(func=cmd_control_tower_status)

    roster_parser = subparsers.add_parser("council-roster-status", help="Summarize the current council roster.")
    roster_parser.add_argument("--json", action="store_true")
    roster_parser.set_defaults(func=cmd_council_roster_status)

    subagent_parser = subparsers.add_parser("subagent-status", help="Summarize the v16 subagent registry.")
    subagent_parser.add_argument("--json", action="store_true")
    subagent_parser.set_defaults(func=cmd_subagent_status)

    multi_instance_parser = subparsers.add_parser("multi-instance-status", help="Summarize the bounded local multi-instance registry.")
    multi_instance_parser.add_argument("--json", action="store_true")
    multi_instance_parser.set_defaults(func=cmd_multi_instance_status)

    codex_adapter_parser = subparsers.add_parser("codex-adapter-status", help="Summarize the repo-first Codex subagent adapter.")
    codex_adapter_parser.add_argument("--json", action="store_true")
    codex_adapter_parser.set_defaults(func=cmd_codex_adapter_status)

    agent_mesh_parser = subparsers.add_parser("agent-mesh-status", help="Summarize the repo-first Codex agent mesh.")
    agent_mesh_parser.add_argument("--json", action="store_true")
    agent_mesh_parser.set_defaults(func=cmd_agent_mesh_status)

    github_parser = subparsers.add_parser("github-status", help="Check current branch and remote reachability.")
    github_parser.add_argument("--json", action="store_true")
    github_parser.set_defaults(func=cmd_github_status)

    docker_parser = subparsers.add_parser("docker-status", help="Check Docker container visibility.")
    docker_parser.add_argument("--json", action="store_true")
    docker_parser.set_defaults(func=cmd_docker_status)

    postgres_parser = subparsers.add_parser("postgres-status", help="Check local Postgres container readiness.")
    postgres_parser.add_argument("--json", action="store_true")
    postgres_parser.set_defaults(func=cmd_postgres_status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
