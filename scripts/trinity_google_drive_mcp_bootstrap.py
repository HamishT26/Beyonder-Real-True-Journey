#!/usr/bin/env python3
"""Bootstrap the bounded Google Drive MCP path for Trinity v11."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CODEX_CONFIG = Path.home() / ".codex" / "config.toml"
SECRETS_DIR = Path.home() / ".codex" / "secrets" / "google-drive-mcp"
SECRETS_FILE = SECRETS_DIR / "gcp-oauth.keys.json"
DEFAULT_SOURCE = Path.home() / "Downloads" / "gcp-oauth.keys.json"
DOCKER_VOLUME = "mcp-gdrive"
ACTIVATION_JSON = ROOT / "docs" / "trinity-google-drive-mcp-activation-latest.json"
ACTIVATION_MD = ROOT / "docs" / "trinity-google-drive-mcp-activation-latest.md"
MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v9.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(args=args, returncode=124, stdout=exc.stdout or "", stderr=(exc.stderr or "") + f"\ncommand timed out after {timeout} seconds")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_secret(source: Path) -> tuple[bool, str]:
    if not source.exists():
        return False, f"oauth source missing: {source}"
    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    if not SECRETS_FILE.exists() or source.resolve() != SECRETS_FILE.resolve():
        shutil.copy2(source, SECRETS_FILE)
    return True, str(SECRETS_FILE)


def ensure_volume() -> tuple[bool, str]:
    inspect_proc = run(["docker", "volume", "inspect", DOCKER_VOLUME], timeout=20)
    if inspect_proc.returncode == 0:
        return True, "existing"
    create_proc = run(["docker", "volume", "create", DOCKER_VOLUME], timeout=20)
    if create_proc.returncode == 0:
        return True, "created"
    return False, create_proc.stderr.strip() or create_proc.stdout.strip()


def ensure_docker_health() -> tuple[bool, str]:
    version_proc = run(["docker", "version", "--format", "{{.Server.Version}}"], timeout=20)
    if version_proc.returncode == 0 and version_proc.stdout.strip():
        return True, version_proc.stdout.strip()
    detail = version_proc.stderr.strip() or version_proc.stdout.strip() or "docker daemon unavailable"
    return False, detail


def ensure_image() -> tuple[bool, str]:
    inspect_proc = run(["docker", "image", "inspect", "mcp/gdrive"], timeout=20)
    if inspect_proc.returncode == 0:
        return True, "present"
    pull_proc = run(["docker", "pull", "mcp/gdrive"], timeout=40)
    if pull_proc.returncode == 0:
        return True, "pulled"
    return False, pull_proc.stderr.strip() or pull_proc.stdout.strip() or "docker image unavailable"


def update_codex_config() -> tuple[bool, str]:
    CODEX_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    existing = CODEX_CONFIG.read_text(encoding="utf-8") if CODEX_CONFIG.exists() else ""
    secret_path = str(SECRETS_FILE).replace("\\", "/")
    block = "\n".join(
        [
            "[mcp_servers.google_drive]",
            "command = 'docker.exe'",
            "args = ['run', '-i', '--rm', '-v', 'mcp-gdrive:/gdrive-server', '--mount', 'type=bind,src=" + secret_path + ",dst=/gcp-oauth.keys.json,readonly', 'mcp/gdrive']",
            "",
        ]
    )
    pattern = re.compile(r"(?ms)^\[mcp_servers\.google_drive\]\n.*?(?=^\[|\Z)")
    if pattern.search(existing):
        updated = pattern.sub(block, existing).rstrip() + "\n"
        CODEX_CONFIG.write_text(updated, encoding="utf-8")
        return True, "updated"
    CODEX_CONFIG.write_text(existing.rstrip() + "\n\n" + block, encoding="utf-8")
    return True, "appended"


def update_catalog(overall_status: str, oauth_seeded: bool, volume_state: str, config_state: str, blockers: list[str]) -> None:
    if not MCP_CATALOG.exists():
        return
    payload = json.loads(MCP_CATALOG.read_text(encoding="utf-8"))
    connectors = payload.get("connectors", [])
    if not isinstance(connectors, list):
        return
    for row in connectors:
        if isinstance(row, dict) and str(row.get("mcp_id")) == "google_drive":
            row["status"] = "staged_setup_gate" if blockers else "verified_live"
            row["actual_state"] = "staged_setup_gate" if blockers else "bounded_archive_mirror"
            row["live_read_enabled"] = False
            row["live_write_enabled"] = False
            row["archive_only"] = True
            row["oauth_bootstrap_state"] = "seeded" if oauth_seeded else "missing"
            row["docker_volume_state"] = volume_state
            row["fallback_mode"] = "memory_bank_archive_only"
            row["blockers"] = blockers
            row["last_verified_utc"] = now_iso()
            row["promotion_evidence"] = [] if blockers else [str(ACTIVATION_JSON.relative_to(ROOT)).replace("\\", "/")]
            row["notes"] = "Docker-first Google Drive MCP path bootstrapped locally." if not blockers else "Docker-first Google Drive MCP path seeded locally, but auth/bootstrap still blocked."
    payload["generated_utc"] = now_iso()
    write_json(MCP_CATALOG, payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap the Docker-first Google Drive MCP path.")
    parser.add_argument("--oauth-source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--seed-secrets", action="store_true")
    parser.add_argument("--update-config", action="store_true")
    args = parser.parse_args()

    blockers: list[str] = []
    oauth_seeded = False
    oauth_detail = "not_attempted"
    if args.seed_secrets:
        oauth_seeded, oauth_detail = ensure_secret(Path(args.oauth_source))
        if not oauth_seeded:
            blockers.append(oauth_detail)

    docker_ok, docker_state = ensure_docker_health()
    if not docker_ok:
        blockers.append(f"docker daemon error: {docker_state}")
        volume_ok, volume_state = False, "daemon_unreachable"
        image_ok, image_state = False, "daemon_unreachable"
    else:
        volume_ok, volume_state = ensure_volume()
        if not volume_ok:
            blockers.append(f"docker volume error: {volume_state}")

        image_ok, image_state = ensure_image()
        if not image_ok:
            blockers.append(f"docker image error: {image_state}")

    config_ok = False
    config_state = "not_attempted"
    if args.update_config:
        config_ok, config_state = update_codex_config()
        if not config_ok:
            blockers.append(f"config update error: {config_state}")

    blockers.append("interactive OAuth bootstrap still required to complete Drive auth")
    overall_status = "WARN" if blockers else "PASS"
    payload = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "docker_first_path": True,
        "docker_daemon_state": docker_state if docker_ok else "error",
        "oauth_source": str(Path(args.oauth_source)),
        "oauth_secret_target": str(SECRETS_FILE),
        "oauth_secret_seeded": oauth_seeded,
        "oauth_seed_detail": oauth_detail,
        "docker_volume_name": DOCKER_VOLUME,
        "docker_volume_state": volume_state if volume_ok else "error",
        "docker_image_state": image_state if image_ok else "error",
        "config_entry_state": config_state if config_ok else "pending",
        "auth_bootstrap_state": "pending_interactive_oauth",
        "fallback_mode": "memory_bank_archive_only",
        "blockers": blockers,
    }
    write_json(ACTIVATION_JSON, payload)
    write_text(
        ACTIVATION_MD,
        "\n".join(
            [
                "# Trinity Google Drive MCP Activation",
                "",
                f"- overall_status: `{overall_status}`",
                f"- oauth_secret_seeded: `{oauth_seeded}`",
                f"- docker_daemon_state: `{docker_state if docker_ok else 'error'}`",
                f"- docker_volume_state: `{volume_state if volume_ok else 'error'}`",
                f"- docker_image_state: `{image_state if image_ok else 'error'}`",
                f"- config_entry_state: `{config_state if config_ok else 'pending'}`",
                "- auth_bootstrap_state: `pending_interactive_oauth`",
                "- fallback_mode: `memory_bank_archive_only`",
                "",
                "## Blockers",
                *[f"- {item}" for item in blockers],
                "",
            ]
        ),
    )
    update_catalog(overall_status, oauth_seeded, volume_state if volume_ok else "error", config_state if config_ok else "pending", blockers)
    print(f"overall_status={overall_status}")
    print(f"latest_json={ACTIVATION_JSON.relative_to(ROOT)}")
    print(f"latest_md={ACTIVATION_MD.relative_to(ROOT)}")
    return 0 if overall_status == "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
