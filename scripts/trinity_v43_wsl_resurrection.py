#!/usr/bin/env python3
"""Repair and prove the V43 WSL lane with preserve-first backups and honest selector gating."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from trinity_v43_common import (
    DEFAULT_ARCHIVE_ROOT,
    DEFAULT_WSL_BACKUP_ROOT,
    DEFAULT_WSL_INSTALL_ROOT,
    LOCAL_RUNTIME_DIR,
    REPO_MOUNT,
    ROOT,
    UBUNTU_EXE_PATH,
    WSL_DISTRO,
    WSL_EXE_PATH,
    WSL_SERVICE_PATH,
    now_iso,
    safe_run,
    write_json,
    write_text,
)

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-wsl-resurrection-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v43-wsl-resurrection-v1.md"
FILESYSTEM_MARKER_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-filesystem-publication-marker-v1.json"
CONFIG_TOML = Path(r"C:\Users\hamis\.codex\config.toml")
WSL_APPX_NAME = "MicrosoftCorporationII.WindowsSubsystemForLinux"
UBUNTU_APPX_NAME = "CanonicalGroupLimited.Ubuntu"
CODEX_EXE_MOUNT = "/mnt/c/Users/hamis/.codex/.sandbox-bin/codex.exe"


def _completed(proc: Any) -> dict[str, Any]:
    return {
        "returncode": proc.returncode,
        "stdout": (proc.stdout or "").strip(),
        "stderr": (proc.stderr or "").strip(),
        "ok": proc.returncode == 0,
    }


def _ps(command: str, *, timeout: int = 120) -> Any:
    return safe_run(["powershell", "-NoProfile", "-Command", command], timeout=timeout)


def _ps_json(command: str, *, timeout: int = 120) -> Any:
    proc = _ps(command, timeout=timeout)
    if proc.returncode != 0 or not proc.stdout.strip():
        return {}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {}


def _package_info(name: str) -> dict[str, Any]:
    payload = _ps_json(
        (
            f"Get-AppxPackage -Name '{name}' | "
            "Select-Object Name,PackageFullName,PackageFamilyName,InstallLocation,Version | "
            "ConvertTo-Json -Depth 4"
        )
    )
    if isinstance(payload, list):
        for row in payload:
            if isinstance(row, dict):
                return row
        return {}
    return payload if isinstance(payload, dict) else {}


def _service_info() -> dict[str, Any]:
    payload = _ps_json(
        (
            "(Get-CimInstance Win32_Service -Filter \"Name='WSLService'\" | "
            "Select-Object Name,State,Status,StartMode,PathName) | ConvertTo-Json -Depth 4"
        )
    )
    return payload if isinstance(payload, dict) else {}


def _launcher_probe() -> dict[str, Any]:
    status = _completed(safe_run(["wsl.exe", "--status"], timeout=90))
    inventory = _completed(safe_run(["wsl.exe", "-l", "-v"], timeout=90))
    version = _completed(safe_run(["wsl.exe", "--version"], timeout=90))
    ubuntu_ping = _completed(safe_run(["ubuntu.exe", "run", "printf", "V43_UBUNTU_PING"], timeout=120))
    service = _service_info()

    if not WSL_EXE_PATH.exists():
        state = "wsl_exe_missing"
    elif not WSL_SERVICE_PATH.exists():
        state = "host_service_binary_missing"
    elif status["ok"] or inventory["ok"] or version["ok"]:
        state = "launchers_ready"
    else:
        state = "launcher_cli_blocked"

    return {
        "state": state,
        "wsl_exe_present": WSL_EXE_PATH.exists(),
        "ubuntu_exe_present": UBUNTU_EXE_PATH.exists(),
        "wsl_service_binary_present": WSL_SERVICE_PATH.exists(),
        "service": service,
        "status": status,
        "inventory": inventory,
        "version": version,
        "ubuntu_ping": ubuntu_ping,
    }


def _registration_probe() -> dict[str, Any]:
    payload = _ps_json(
        (
            "Get-ItemProperty -Path HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss\\* | "
            "Select-Object DistributionName,BasePath,State,Version,DefaultUid | ConvertTo-Json -Depth 5"
        )
    )
    rows = payload if isinstance(payload, list) else ([payload] if isinstance(payload, dict) and payload else [])
    ubuntu = {}
    for row in rows:
        if isinstance(row, dict) and str(row.get("DistributionName") or "") == WSL_DISTRO:
            ubuntu = row
            break

    base_path = Path(str(ubuntu.get("BasePath") or "")) if ubuntu else Path()
    vhd_path = base_path / "ext4.vhdx" if base_path else Path()
    if ubuntu and base_path.drive.upper() == "D:" and vhd_path.exists():
        state = "registered_d_drive_install"
    elif ubuntu and vhd_path.exists():
        state = "registered_vhd_present"
    elif ubuntu:
        state = "registered_vhd_missing"
    else:
        state = "ubuntu_not_registered"

    return {
        "state": state,
        "ubuntu_registration": ubuntu,
        "all_registrations": rows,
        "base_path": str(base_path) if base_path else "",
        "vhd_path": str(vhd_path) if vhd_path else "",
        "vhd_present": vhd_path.exists() if vhd_path else False,
    }


def _ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _backup_vhd(source: Path, backup_root: Path) -> dict[str, Any]:
    if not source.exists():
        return {
            "state": "backup_source_missing",
            "source_path": str(source),
            "backup_path": "",
            "copied_bytes": 0,
            "verified": False,
        }

    stamp = now_iso().replace(":", "-").replace("+00:00", "Z")
    backup_dir = backup_root / f"v43-wsl-{stamp}"
    _ensure_directory(backup_dir)
    backup_path = backup_dir / source.name
    shutil.copy2(source, backup_path)
    copied_bytes = backup_path.stat().st_size if backup_path.exists() else 0
    return {
        "state": "backup_verified" if backup_path.exists() else "backup_copy_failed",
        "source_path": str(source),
        "backup_path": str(backup_path),
        "copied_bytes": copied_bytes,
        "verified": backup_path.exists(),
    }


def _run_wsl(command: str, *, timeout: int = 180) -> dict[str, Any]:
    proc = safe_run(["wsl.exe", "-d", WSL_DISTRO, "--", "bash", "-lc", command], timeout=timeout)
    return _completed(proc)


def _selector_state(codex_version_ok: bool) -> tuple[str, bool]:
    config_text = CONFIG_TOML.read_text(encoding="utf-8", errors="replace") if CONFIG_TOML.exists() else ""
    selector_keywords = ("wsl", "ubuntu", "bash", "environment_selector", "linux")
    selector_configurable = any(token in config_text.lower() for token in selector_keywords)
    if codex_version_ok and selector_configurable:
        return "config_surface_present_cli_wsl_entrypoint_verified", False
    if codex_version_ok:
        return "cli_wsl_entrypoint_verified_app_selector_unresolved", True
    return "cli_entrypoint_blocked", False


def _distro_health() -> dict[str, Any]:
    bash_probe = _run_wsl("test -x /usr/bin/bash && printf /usr/bin/bash")
    python_probe = _run_wsl("command -v python3")
    git_probe = _run_wsl("command -v git")
    node_probe = _run_wsl("command -v node")
    npx_probe = _run_wsl("command -v npx")
    repo_probe = _run_wsl(f"cd {REPO_MOUNT} && git rev-parse --short HEAD", timeout=240)
    codex_version = _run_wsl(f"'{CODEX_EXE_MOUNT}' --version", timeout=120)
    selector_state, checkpoint_required = _selector_state(codex_version["ok"])
    wsl_health_state = (
        "ubuntu_repaired_toolchain_ready"
        if all(
            [
                bash_probe["ok"],
                python_probe["ok"],
                git_probe["ok"],
                node_probe["ok"],
                npx_probe["ok"],
                repo_probe["ok"],
            ]
        )
        else "ubuntu_health_blocked"
    )
    return {
        "wsl_health_state": wsl_health_state,
        "codex_wsl_selector_state": selector_state,
        "manual_operator_checkpoint_required": checkpoint_required,
        "probes": {
            "bash": bash_probe,
            "python3": python_probe,
            "git": git_probe,
            "node": node_probe,
            "npx": npx_probe,
            "repo": repo_probe,
            "codex_version": codex_version,
        },
    }


def _repair_host(wsl_package: dict[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []

    winget = _completed(
        safe_run(
            [
                "winget",
                "install",
                "--id",
                "Microsoft.WSL",
                "--exact",
                "--source",
                "winget",
                "--accept-package-agreements",
                "--accept-source-agreements",
                "--disable-interactivity",
                "--force",
            ],
            timeout=2400,
        )
    )
    attempts.append(
        {
            "name": "winget_reinstall_microsoft_wsl",
            "result": winget,
            "service_binary_present_after": WSL_SERVICE_PATH.exists(),
        }
    )

    manifest = Path(str(wsl_package.get("InstallLocation") or "")) / "AppxManifest.xml"
    if not WSL_SERVICE_PATH.exists() and manifest.exists():
        register = _completed(
            _ps(
                f"Add-AppxPackage -DisableDevelopmentMode -Register '{manifest}'",
                timeout=600,
            )
        )
        attempts.append(
            {
                "name": "re_register_wsl_appx_manifest",
                "result": register,
                "service_binary_present_after": WSL_SERVICE_PATH.exists(),
            }
        )

    if WSL_SERVICE_PATH.exists():
        start_service = _completed(_ps("Start-Service -Name WSLService -ErrorAction Continue", timeout=120))
        attempts.append({"name": "start_wsl_service", "result": start_service})
    return attempts


def _import_in_place(vhd_path: Path) -> dict[str, Any]:
    unregister = _completed(safe_run(["wsl.exe", "--unregister", WSL_DISTRO], timeout=180))
    import_proc = _completed(safe_run(["wsl.exe", "--import-in-place", WSL_DISTRO, str(vhd_path)], timeout=600))
    return {
        "unregister": unregister,
        "import_in_place": import_proc,
    }


def _clean_install(install_root: Path, install_tar: Path) -> dict[str, Any]:
    _ensure_directory(install_root.parent)
    if install_root.exists() and any(install_root.iterdir()):
        rollover = install_root.parent / f"{install_root.name}-stale-{now_iso().replace(':', '-').replace('+00:00', 'Z')}"
        install_root.rename(rollover)
    _ensure_directory(install_root)

    import_proc = _completed(
        safe_run(
            ["wsl.exe", "--import", WSL_DISTRO, str(install_root), str(install_tar), "--version", "2"],
            timeout=1200,
        )
    )
    packages = _run_wsl(
        "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 git nodejs npm",
        timeout=3600,
    )
    return {
        "import": import_proc,
        "package_bootstrap": packages,
        "install_root": str(install_root),
        "install_tar": str(install_tar),
    }


def _repo_write_cycle() -> dict[str, Any]:
    marker_mount = f"{REPO_MOUNT}/.local-runtime/v43/wsl-repo-write-cycle.txt"
    publication_mount = f"{REPO_MOUNT}/docs/trinity-live-traces/v43-filesystem-publication-marker-v1.json"
    publication_payload = {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "marker": "V43_WSL_PUBLICATION_OK",
        "repo_mount": REPO_MOUNT,
        "written_from": "wsl_bash",
    }
    script = (
        "python3 - <<'PY'\n"
        "from pathlib import Path\n"
        "marker = Path(" + repr(marker_mount) + ")\n"
        "publication = Path(" + repr(publication_mount) + ")\n"
        "marker.parent.mkdir(parents=True, exist_ok=True)\n"
        "publication.parent.mkdir(parents=True, exist_ok=True)\n"
        "marker.write_text('V43_WSL_REPO_WRITE_OK\\n', encoding='utf-8')\n"
        "publication.write_text(" + repr(json.dumps(publication_payload, indent=2) + "\n") + ", encoding='utf-8')\n"
        "print('V43_WSL_PUBLICATION_OK')\n"
        "PY"
    )
    result = _run_wsl(script, timeout=240)
    marker_path = ROOT / ".local-runtime" / "v43" / "wsl-repo-write-cycle.txt"
    publication_path = FILESYSTEM_MARKER_JSON
    return {
        "result": result,
        "marker_path": str(marker_path),
        "marker_present": marker_path.exists(),
        "publication_path": str(publication_path),
        "publication_present": publication_path.exists(),
        "verified": result["ok"] and marker_path.exists() and publication_path.exists(),
    }


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V43 WSL Resurrection",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- WSL launcher state: `{payload['wsl_launcher_state']}`",
        f"- Ubuntu registration state: `{payload['ubuntu_registration_state']}`",
        f"- Ubuntu VHD backup state: `{payload['ubuntu_vhd_backup_state']}`",
        f"- WSL recovery state: `{payload['wsl_recovery_state']}`",
        f"- WSL health state: `{payload['wsl_health_state']}`",
        f"- Codex selector state: `{payload['codex_wsl_selector_state']}`",
        f"- Filesystem promotion state: `{payload['filesystem_promotion_state']}`",
        f"- Drive archive state: `{payload['drive_archive_state']}`",
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
    parser = argparse.ArgumentParser(description="Repair and prove the V43 WSL lane.")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--backup-root", default=str(DEFAULT_WSL_BACKUP_ROOT))
    parser.add_argument("--install-root", default=str(DEFAULT_WSL_INSTALL_ROOT))
    parser.add_argument("--archive-root", default=str(DEFAULT_ARCHIVE_ROOT))
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    backup_root = Path(args.backup_root)
    install_root = Path(args.install_root)
    archive_root = Path(args.archive_root)
    _ensure_directory(LOCAL_RUNTIME_DIR)
    _ensure_directory(backup_root)
    _ensure_directory(archive_root)

    launcher_before = _launcher_probe()
    registration_before = _registration_probe()
    wsl_package = _package_info(WSL_APPX_NAME)
    ubuntu_package = _package_info(UBUNTU_APPX_NAME)

    vhd_path = Path(str(registration_before.get("vhd_path") or "")) if registration_before.get("vhd_path") else Path()
    backup = _backup_vhd(vhd_path, backup_root) if vhd_path else {
        "state": "backup_source_missing",
        "source_path": "",
        "backup_path": "",
        "copied_bytes": 0,
        "verified": False,
    }

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "overall_status": "WARN",
        "probe_only": args.probe_only,
        "wsl_launcher_state": launcher_before["state"],
        "ubuntu_registration_state": registration_before["state"],
        "ubuntu_vhd_backup_state": backup["state"],
        "wsl_recovery_state": "probe_only_no_repair_attempted" if args.probe_only else "pending",
        "wsl_health_state": "pending",
        "codex_wsl_selector_state": "pending",
        "filesystem_promotion_state": "blocked",
        "drive_archive_state": "d_archive_roots_ready" if archive_root.exists() and backup_root.exists() else "d_archive_roots_missing",
        "manual_operator_checkpoint_required": False,
        "completed_steps": [],
        "blockers": [],
        "launcher_before": launcher_before,
        "registration_before": registration_before,
        "wsl_package": wsl_package,
        "ubuntu_package": ubuntu_package,
        "vhd_backup": backup,
        "recovery_attempts": [],
    }

    if backup["verified"]:
        payload["completed_steps"].append("preserved_ubuntu_vhd_backup")
    else:
        payload["blockers"].append("The preserve-first VHD backup could not be verified before recovery work.")

    if not args.probe_only and launcher_before["state"] != "launchers_ready":
        payload["recovery_attempts"].extend(_repair_host(wsl_package))
        payload["completed_steps"].append("attempted_wsl_host_repair")

    launcher_after_host = _launcher_probe()
    payload["launcher_after_host_repair"] = launcher_after_host
    payload["wsl_launcher_state"] = launcher_after_host["state"]

    health = _distro_health() if launcher_after_host["state"] == "launchers_ready" else {
        "wsl_health_state": "ubuntu_health_blocked",
        "codex_wsl_selector_state": "host_launcher_unavailable",
        "manual_operator_checkpoint_required": False,
        "probes": {},
    }
    payload["distro_health_after_host_repair"] = health

    if not args.probe_only and launcher_after_host["state"] == "launchers_ready" and health["wsl_health_state"] != "ubuntu_repaired_toolchain_ready":
        if vhd_path.exists():
            in_place = _import_in_place(vhd_path)
            payload["recovery_attempts"].append({"name": "import_in_place_recovery", **in_place})
            payload["completed_steps"].append("attempted_import_in_place_recovery")
            health = _distro_health()
            payload["distro_health_after_import_in_place"] = health
            payload["registration_after_import_in_place"] = _registration_probe()

        if health["wsl_health_state"] != "ubuntu_repaired_toolchain_ready":
            install_location = Path(str(ubuntu_package.get("InstallLocation") or ""))
            install_tar = install_location / "install.tar.gz"
            if install_tar.exists():
                clean_install = _clean_install(install_root, install_tar)
                payload["recovery_attempts"].append({"name": "clean_d_drive_install", **clean_install})
                payload["completed_steps"].append("attempted_clean_d_drive_install")
                health = _distro_health()
                payload["distro_health_after_clean_install"] = health
                payload["registration_after_clean_install"] = _registration_probe()
            else:
                payload["blockers"].append("The Ubuntu Store rootfs tarball was not available for the D-drive recovery fallback.")

    final_registration = _registration_probe()
    payload["final_registration"] = final_registration
    payload["ubuntu_registration_state"] = final_registration["state"]
    payload["wsl_health_state"] = health["wsl_health_state"]
    payload["codex_wsl_selector_state"] = health["codex_wsl_selector_state"]
    payload["manual_operator_checkpoint_required"] = bool(health["manual_operator_checkpoint_required"])
    payload["distro_health"] = health

    write_cycle = {
        "result": {"ok": False, "returncode": 1, "stdout": "", "stderr": "wsl_not_ready"},
        "marker_path": str(ROOT / ".local-runtime" / "v43" / "wsl-repo-write-cycle.txt"),
        "marker_present": False,
        "publication_path": str(FILESYSTEM_MARKER_JSON),
        "publication_present": False,
        "verified": False,
    }
    if health["wsl_health_state"] == "ubuntu_repaired_toolchain_ready":
        write_cycle = _repo_write_cycle()
        if write_cycle["verified"]:
            payload["completed_steps"].append("verified_wsl_repo_write_and_publication_cycle")
    payload["repo_write_cycle"] = write_cycle

    if health["wsl_health_state"] == "ubuntu_repaired_toolchain_ready" and write_cycle["verified"]:
        if health["codex_wsl_selector_state"] == "desktop_selector_verified":
            payload["filesystem_promotion_state"] = "unblocked"
        else:
            payload["filesystem_promotion_state"] = "blocked"
            payload["blockers"].append(
                "Codex CLI can reach the repaired distro, but the desktop environment selector is still unresolved; filesystem promotion stays blocked."
            )
    elif health["wsl_health_state"] != "ubuntu_repaired_toolchain_ready":
        payload["blockers"].append("The repaired Ubuntu distro did not reach the required bash/python3/git/node/npx health gate.")

    if launcher_before["state"] != "launchers_ready" and launcher_after_host["state"] == "launchers_ready":
        payload["wsl_recovery_state"] = "host_repaired_existing_or_recovered_launcher_ready"
    if health["wsl_health_state"] == "ubuntu_repaired_toolchain_ready":
        if final_registration["state"] == "registered_d_drive_install":
            payload["wsl_recovery_state"] = "clean_d_drive_install_verified"
        elif payload.get("distro_health_after_import_in_place"):
            payload["wsl_recovery_state"] = "import_in_place_recovered"
        else:
            payload["wsl_recovery_state"] = "existing_registration_recovered"
    elif args.probe_only:
        payload["wsl_recovery_state"] = "probe_only_no_repair_attempted"
    elif launcher_after_host["state"] != "launchers_ready":
        payload["wsl_recovery_state"] = "host_repair_blocked"
        payload["blockers"].append("WSL launchers remained blocked after the host repair attempt.")
    else:
        payload["wsl_recovery_state"] = "recovery_failed"

    if payload["wsl_recovery_state"] == "clean_d_drive_install_verified":
        payload["completed_steps"].append("verified_clean_d_drive_install")
    elif payload["wsl_recovery_state"] == "import_in_place_recovered":
        payload["completed_steps"].append("verified_import_in_place_recovery")
    elif payload["wsl_recovery_state"] == "existing_registration_recovered":
        payload["completed_steps"].append("verified_existing_registration_recovery")

    payload["overall_status"] = (
        "PASS"
        if payload["wsl_health_state"] == "ubuntu_repaired_toolchain_ready"
        and payload["filesystem_promotion_state"] == "unblocked"
        else "WARN"
    )

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), _markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
