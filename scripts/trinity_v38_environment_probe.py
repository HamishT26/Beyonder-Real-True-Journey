#!/usr/bin/env python3
"""Validate the named V38 Codex environment as an operator surface."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
AUTHORITATIVE_REPO = Path(r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey")
WORKBENCH_REPO = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
CODEX_HOME = Path.home() / ".codex"
ENVIRONMENT_NAME = "Beyonder-Real-True Journey"
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v38-environment-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v38-environment-proof-v1.md"


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=(exc.stdout or "") if isinstance(exc.stdout, str) else "",
            stderr=((exc.stderr or "") if isinstance(exc.stderr, str) else "") + f"\ncommand timed out after {timeout} seconds",
        )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git_top_level(path: Path) -> str:
    probe = run(["git", "-C", str(path), "rev-parse", "--show-toplevel"])
    return (probe.stdout or "").strip() if probe.returncode == 0 else ""


def normalized_path(text: str) -> str:
    if not text:
        return ""
    try:
        return str(Path(text).resolve())
    except OSError:
        return str(Path(text))


def search_codex_environment_refs() -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    if not CODEX_HOME.exists():
        return hits
    allowed_suffixes = {".toml", ".md", ".json"}
    for path in CODEX_HOME.rglob("*"):
        if len(hits) >= 20:
            break
        if not path.is_file() or path.suffix.lower() not in allowed_suffixes:
            continue
        if path.stat().st_size > 1_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if ENVIRONMENT_NAME.lower() not in text.lower():
            continue
        rel = str(path.relative_to(CODEX_HOME)).replace("\\", "/")
        hits.append({"path": rel, "kind": path.suffix.lower()})
    return hits


def load_catalog_workspace_target() -> dict[str, Any]:
    for rel in ("docs/trinity-mcp-catalog-v11.json", "docs/trinity-mcp-catalog-v9.json"):
        catalog = ROOT / rel
        if not catalog.exists():
            continue
        payload = json.loads(catalog.read_text(encoding="utf-8-sig"))
        workspace_target = str(payload.get("workspace_target") or "")
        if not workspace_target and isinstance(payload.get("connectors"), list):
            for row in payload["connectors"]:
                if not isinstance(row, dict):
                    continue
                target = str(row.get("workspace_target") or "")
                if target == ENVIRONMENT_NAME:
                    workspace_target = target
                    break
        return {
            "path": str(catalog.relative_to(ROOT)).replace("\\", "/"),
            "workspace_target": workspace_target,
            "present": True,
        }
    return {
        "path": "docs/trinity-mcp-catalog-v11.json",
        "workspace_target": "",
        "present": True,
    }


def build_payload() -> dict[str, Any]:
    codex_hits = search_codex_environment_refs()
    catalog = load_catalog_workspace_target()
    repo_top = git_top_level(AUTHORITATIVE_REPO)
    workbench_top = git_top_level(WORKBENCH_REPO)
    python_probe = run(["python", "--version"])
    git_probe = run(["git", "--version"])

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "environment_name": ENVIRONMENT_NAME,
        "authoritative_repo_path": str(AUTHORITATIVE_REPO),
        "workbench_repo_path": str(WORKBENCH_REPO),
        "codex_environment_state": "pending",
        "overall_status": "WARN",
        "completed_steps": [],
        "blockers": [],
        "host_surface": {
            "platform": platform.platform(),
            "python_executable": os.sys.executable,
            "cwd": str(Path.cwd()),
            "code_home_present": CODEX_HOME.exists(),
            "config_toml_present": (CODEX_HOME / "config.toml").exists(),
            "skills_dir_present": (CODEX_HOME / "skills").exists(),
            "plugin_cache_present": (CODEX_HOME / "plugins" / "cache").exists(),
        },
        "authoritative_repo_probe": {
            "path_exists": AUTHORITATIVE_REPO.exists(),
            "git_top_level": repo_top,
            "mounted_visible": normalized_path(repo_top) == normalized_path(str(AUTHORITATIVE_REPO)),
        },
        "workbench_probe": {
            "path_exists": WORKBENCH_REPO.exists(),
            "git_top_level": workbench_top,
            "separate_from_authority": normalized_path(workbench_top) == normalized_path(str(WORKBENCH_REPO)),
        },
        "tooling_probe": {
            "python": {"returncode": python_probe.returncode, "stdout": (python_probe.stdout or python_probe.stderr or "").strip()},
            "git": {"returncode": git_probe.returncode, "stdout": (git_probe.stdout or git_probe.stderr or "").strip()},
        },
        "catalog_workspace_target": catalog,
        "codex_environment_hits": codex_hits,
        "codex_environment_hit_count": len(codex_hits),
    }

    if payload["authoritative_repo_probe"]["mounted_visible"]:
        payload["completed_steps"].append("authoritative_repo_mount_verified")
    else:
        payload["blockers"].append("The authoritative repo is not visible as the active git top-level from the canonical path.")

    if payload["host_surface"]["code_home_present"] and payload["host_surface"]["config_toml_present"]:
        payload["completed_steps"].append("codex_surface_reachable")
    else:
        payload["blockers"].append("The local .codex surface is not fully reachable from the current environment.")

    if python_probe.returncode == 0 and git_probe.returncode == 0:
        payload["completed_steps"].append("shell_readiness_verified")
    else:
        payload["blockers"].append("Python or git failed its basic version probe inside the current environment.")

    if catalog.get("workspace_target") == ENVIRONMENT_NAME:
        payload["completed_steps"].append("workspace_target_documented")

    if codex_hits:
        payload["completed_steps"].append("environment_name_directly_discovered")
        if not payload["blockers"]:
            payload["codex_environment_state"] = "validated_primary_operator_surface"
            payload["overall_status"] = "PASS"
        else:
            payload["codex_environment_state"] = "discoverable_but_bounded"
            payload["overall_status"] = "WARN"
    else:
        if catalog.get("workspace_target") == ENVIRONMENT_NAME and not payload["blockers"]:
            payload["codex_environment_state"] = "documented_but_not_directly_discoverable"
            payload["overall_status"] = "WARN"
            payload["blockers"].append(
                "The named Codex environment is documented in repo surfaces but not directly discoverable from the local .codex configuration files."
            )
        else:
            payload["codex_environment_state"] = "blocked_environment_visibility"
            payload["overall_status"] = "FAIL"
            payload["blockers"].append("No direct local discovery signal was found for the named Codex environment.")

    payload["primary_operator_surface_ready"] = payload["codex_environment_state"] == "validated_primary_operator_surface"
    return payload


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V38 Environment Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Environment name: `{payload['environment_name']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Codex environment state: `{payload['codex_environment_state']}`",
        f"- Authoritative repo mount visible: `{payload['authoritative_repo_probe']['mounted_visible']}`",
        f"- Direct environment hits: `{payload['codex_environment_hit_count']}`",
        "",
        "## Completed Steps",
        "",
    ]
    lines.extend(f"- `{step}`" for step in payload.get("completed_steps", []))
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    write_text(output_md, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the named V38 Codex environment.")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    payload = build_payload()
    write_outputs(payload, Path(args.output_json), Path(args.output_md))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
