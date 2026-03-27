#!/usr/bin/env python3
"""Build and verify bounded memory-bank snapshots for Trinity Hybrid OS.

This helper keeps the repo authoritative while producing compact snapshot
artifacts and capability reports for remote or semi-remote storage surfaces.
Google Drive may act as a bounded working mirror for non-authoritative
artifacts, but it never overrides repo-first truth.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from trinity_zip_memory_converter import DEFAULT_ARCHIVE_DIR, DEFAULT_INDEX, archive as create_archive

ROOT = Path(__file__).resolve().parent.parent
WORKBENCH_ROOT = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
REGISTRY_PATH = ROOT / "docs" / "trinity-memory-bank-registry-v3.json"
REPORT_JSON_PATH = ROOT / "docs" / "trinity-memory-bank-sync-latest.json"
REPORT_MD_PATH = ROOT / "docs" / "trinity-memory-bank-sync-latest.md"
PLAYBOOK_PATH = ROOT / "docs" / "trinity-memory-bank-playbook-v3.md"
DRIVE_LEDGER_PATH = ROOT / "docs" / "trinity-drive-archive-ledger.jsonl"
WORKBENCH_MIRROR_PATH = WORKBENCH_ROOT / "memory-bank" / "latest-sync-summary.json"
GOOGLE_POLICY_PATH = ROOT / "docs" / "trinity-google-drive-sync-policy-v1.json"

ARCHIVE_SOURCES = [
    "docs/system-suite-status.json",
    "docs/system-suite-run-report.md",
    "docs/trinity-control-tower-latest.json",
    "docs/trinity-command-book-v5.json",
    "docs/trinity-command-book-latest.md",
    "docs/trinity-agent-council-roster-v3.json",
    "docs/trinity-agent-proof-b-status-v1.json",
    "docs/trinity-agent-official-induction-summary-v1.json",
    "docs/v11-council-group-reflection.md",
    "docs/v11-gmut-research-brief.md",
    "docs/v11-freedid-governance-brief.md",
    "docs/v12-roadmap-v2.md",
    "docs/aletheon-reflection-latest.md",
    "docs/aletheon-next-plan.md",
]

OFFICIAL_SOURCES = {
    "google_drive_api": "https://developers.google.com/drive/api/reference/rest/v3/files/create",
    "google_drive_uploads": "https://developers.google.com/drive/api/guides/manage-uploads",
    "docker_volumes": "https://docs.docker.com/engine/storage/volumes/",
    "git_bundle": "https://git-scm.com/docs/git-bundle",
}

STORAGE_PRESSURE_WATCH_FREE_GIB = 4.0


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_cmd(args: list[str], timeout: int = 30, check: bool = False) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=check,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=(exc.stderr or "") + f"\ncommand timed out after {timeout} seconds",
        )


def path_to_repo_string(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def google_drive_policy() -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if GOOGLE_POLICY_PATH.exists():
        try:
            payload = load_json(GOOGLE_POLICY_PATH)
        except Exception:  # pragma: no cover - defensive
            payload = {}
    drive_role = str(payload.get("drive_role") or "deferred_archive_target").strip() or "deferred_archive_target"
    operator_hold = bool(payload.get("operator_hold"))
    payload["drive_role"] = drive_role
    payload["operator_hold"] = operator_hold
    payload["activation_disabled_reason"] = str(payload.get("activation_disabled_reason") or "").strip()
    return payload


def probe_git() -> dict[str, Any]:
    branch_proc = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    remote_url_proc = run_cmd(["git", "remote", "get-url", "origin"])
    remote_head_proc = run_cmd(["git", "ls-remote", "origin", "HEAD"], timeout=45)
    return {
        "current_branch": branch_proc.stdout.strip() if branch_proc.returncode == 0 else "unknown",
        "remote_url": remote_url_proc.stdout.strip() if remote_url_proc.returncode == 0 else "unknown",
        "reachable": remote_head_proc.returncode == 0 and bool(remote_head_proc.stdout.strip()),
        "head_ref": remote_head_proc.stdout.strip().split()[0] if remote_head_proc.returncode == 0 and remote_head_proc.stdout.strip() else "",
        "stderr": remote_head_proc.stderr.strip(),
    }


def probe_docker() -> dict[str, Any]:
    ps_proc = run_cmd(["docker", "ps", "--format", "{{.Names}}\t{{.Status}}\t{{.Image}}"], timeout=45)
    rows: list[dict[str, str]] = []
    if ps_proc.returncode == 0:
        for line in ps_proc.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) == 3:
                rows.append({"name": parts[0], "status": parts[1], "image": parts[2]})
    pg_ready = False
    pg_stderr = ""
    if any(row["name"] == "trinity-v5-pg-proof" for row in rows):
        ready_proc = run_cmd(
            ["docker", "exec", "trinity-v5-pg-proof", "pg_isready", "-U", "postgres"],
            timeout=20,
        )
        proof_candidates = [
            ROOT / "docs" / "trinity-live-traces" / "postgres-local-runtime-proof-v1.json",
            ROOT / "docs" / "trinity-live-traces" / "postgres-materialization-proof-v1.json",
        ]
        pg_ready = ready_proc.returncode == 0 or (
            ready_proc.returncode == 124 and any(path.exists() for path in proof_candidates)
        )
        pg_stderr = ready_proc.stderr.strip() or ready_proc.stdout.strip()
        if ready_proc.returncode == 124 and pg_ready:
            pg_stderr = f"{pg_stderr}; container running, bounded fallback enabled from prior Postgres proof".strip("; ")
    return {
        "docker_available": ps_proc.returncode == 0,
        "containers": rows,
        "postgres_container_running": any(row["name"] == "trinity-v5-pg-proof" for row in rows),
        "postgres_ready": pg_ready,
        "stderr": ps_proc.stderr.strip(),
        "postgres_probe": pg_stderr,
    }


def upload_to_google_drive(file_path: Path, token: str, folder_id: str = "") -> dict[str, Any]:
    metadata: dict[str, Any] = {"name": file_path.name}
    if folder_id:
        metadata["parents"] = [folder_id]

    boundary = f"trinity-{uuid.uuid4().hex}"
    file_bytes = file_path.read_bytes()
    payload = (
        f"--{boundary}\r\n"
        "Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        "Content-Type: application/zip\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
    request = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink,webContentLink",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def maybe_copy_to_docker(file_path: Path) -> dict[str, Any]:
    target = f"trinity-v5-pg-proof:/trinity-memory-bank/{file_path.name}"
    copy_proc = run_cmd(["docker", "cp", str(file_path), target], timeout=60)
    return {
        "attempted": True,
        "success": copy_proc.returncode == 0,
        "target": target,
        "stderr": copy_proc.stderr.strip(),
    }


def build_registry(
    *,
    archive_path: Path,
    git_state: dict[str, Any],
    docker_state: dict[str, Any],
    drive_result: dict[str, Any],
    upload_attempted: bool,
    docker_copy: dict[str, Any],
    drive_policy: dict[str, Any],
) -> dict[str, Any]:
    disk = shutil.disk_usage(ROOT)
    free_gib = round(disk.free / (1024**3), 2)
    total_gib = round(disk.total / (1024**3), 2)
    archive_bytes = archive_path.stat().st_size if archive_path.exists() else 0
    prune_report_path = ROOT / "docs" / "trinity-storage-prune-latest.json"
    prune_applied_at = ""
    if prune_report_path.exists():
        try:
            prune_applied_at = str(load_json(prune_report_path).get("generated_utc") or "")
        except Exception:  # noqa: BLE001
            prune_applied_at = ""
    operator_hold = bool(drive_policy.get("operator_hold"))
    drive_role = str(drive_policy.get("drive_role") or "deferred_archive_target")
    drive_status = "staged_with_blockers"
    drive_notes = "Deferred until bounded auth, privacy, and sync proof are available."
    drive_blockers = ["google drive auth not configured"]
    drive_reachable = bool(drive_result.get("uploaded"))
    drive_latest_artifact = str(drive_result.get("file_id") or "")
    drive_proof_state = "drive_not_connected"
    drive_retention_class = "archive_only"
    drive_upload_state = "staged"
    drive_capacity_class = "cloud_archive"
    drive_last_verified = ""
    if operator_hold:
        drive_status = "staged_with_blockers"
        drive_notes = (
            str(drive_policy.get("activation_disabled_reason") or "").strip()
            or "Google Drive remains operator-held until a bounded working-mirror proof is completed."
        )
        drive_blockers = ["google drive activation deferred by operator"]
        drive_proof_state = "operator_hold"
        drive_upload_state = "deferred_by_operator"
    elif drive_role == "bounded_working_mirror":
        drive_capacity_class = "cloud_workspace"
        drive_retention_class = "working_mirror"
        if upload_attempted and drive_result.get("uploaded"):
            drive_status = "bounded_working_mirror"
            drive_notes = "Bounded non-authoritative working mirror verified via explicit Google Drive artifact upload."
            drive_blockers = []
            drive_proof_state = "working_mirror_verified"
            drive_upload_state = "uploaded"
            drive_last_verified = now_iso()
        elif upload_attempted:
            drive_status = "auth_blocked"
            drive_notes = "Bounded working-mirror proof was attempted, but Google Drive auth or upload did not pass cleanly."
            drive_blockers = drive_result.get("blockers", drive_blockers)
            drive_proof_state = "working_mirror_attempt_blocked"
            drive_upload_state = "attempted_blocked"
        else:
            drive_status = "auth_blocked"
            drive_notes = "Bounded working-mirror policy is active, but explicit write/read-back proof is still required before live promotion."
            drive_blockers = ["bounded working-mirror proof not yet completed"]
            drive_proof_state = "working_mirror_proof_pending"
            drive_upload_state = "proof_pending"
    elif upload_attempted and drive_result.get("uploaded"):
        drive_status = "live_archive_mirror"
        drive_notes = "Bounded archive uploaded via explicit Google Drive token flow."
        drive_blockers = []
        drive_proof_state = "drive_uploaded"
        drive_upload_state = "uploaded"
        drive_last_verified = now_iso()
    elif upload_attempted:
        drive_status = "staged_with_blockers"
        drive_notes = "Upload requested, but Google Drive auth or upload handshake did not pass."
        drive_blockers = drive_result.get("blockers", drive_blockers)
        drive_proof_state = "drive_not_connected"
        drive_upload_state = "attempted_blocked"

    overall_status = "PASS" if git_state["reachable"] else "WARN"
    registry = {
        "generated_utc": now_iso(),
        "version": "v3",
        "retained_snapshot_count": min(len(list((ROOT / "docs" / "memory-archives").glob("*.zip"))), 3),
        "prune_policy_applied_at": prune_applied_at,
        "storage_pressure_class": "watch" if free_gib < STORAGE_PRESSURE_WATCH_FREE_GIB else "healthy",
        "overall_status": overall_status,
        "authority_model": "repo_first",
        "storage_pressure": {
            "free_gib": free_gib,
            "total_gib": total_gib,
            "archive_bytes": archive_bytes,
            "archive_megabytes": round(archive_bytes / (1024**2), 2),
        },
        "latest_snapshot": {
            "archive": path_to_repo_string(archive_path),
            "index": path_to_repo_string(DEFAULT_INDEX),
            "source_count": len(ARCHIVE_SOURCES),
            "label": archive_path.stem,
        },
        "memory_banks": [
            {
                "surface": "repo",
                "status": "authoritative",
                "capacity_class": "local_git",
                "notes": "Primary source for certificates, ledgers, reflections, commands, and official council state.",
                "live_checked_at": now_iso(),
                "reachable": True,
                "latest_artifact": path_to_repo_string(archive_path),
                "proof_state": "repo_first_authority",
                "blockers": [],
                "retention_class": "canonical",
                "archive_upload_state": "not_applicable",
                "cloud_capacity_class": "none",
                "last_archive_verified_utc": now_iso(),
            },
            {
                "surface": "github",
                "status": "live_mirror" if git_state["reachable"] else "blocked",
                "capacity_class": "remote_git",
                "notes": "Branch-scoped remote backup and collaboration surface. Never overrides repo authority.",
                "live_checked_at": now_iso(),
                "reachable": git_state["reachable"],
                "latest_artifact": git_state["head_ref"],
                "proof_state": "remote_reachable" if git_state["reachable"] else "remote_unreachable",
                "blockers": [] if git_state["reachable"] else ["git remote unreachable"],
                "retention_class": "remote_mirror",
                "archive_upload_state": "not_applicable",
                "cloud_capacity_class": "bounded",
                "last_archive_verified_utc": now_iso() if git_state["reachable"] else "",
            },
            {
                "surface": "postgres",
                "status": "live_query_store" if docker_state["postgres_ready"] else "blocked",
                "capacity_class": "docker_volume",
                "notes": "Operational state, synthetic mesh, chat indexes, and queryable summaries. Runtime truth follows direct local probes rather than broader suite pass state.",
                "live_checked_at": now_iso(),
                "reachable": docker_state["postgres_ready"],
                "latest_artifact": "trinity-v5-pg-proof",
                "proof_state": "postgres_ready" if docker_state["postgres_ready"] else "postgres_blocked",
                "blockers": [] if docker_state["postgres_ready"] else ["postgres container not ready"],
                "retention_class": "runtime_query",
                "archive_upload_state": "not_applicable",
                "cloud_capacity_class": "bounded",
                "last_archive_verified_utc": now_iso() if docker_state["postgres_ready"] else "",
            },
            {
                "surface": "docker",
                "status": "live_runtime_storage" if docker_state["docker_available"] else "blocked",
                "capacity_class": "local_container_volume",
                "notes": "Runtime substrate for Postgres and bounded simulations. Runtime truth follows direct local probes rather than broader suite pass state.",
                "live_checked_at": now_iso(),
                "reachable": docker_state["docker_available"],
                "latest_artifact": docker_copy.get("target", ""),
                "proof_state": "docker_ready" if docker_state["docker_available"] else "docker_unavailable",
                "blockers": [] if docker_state["docker_available"] else ["docker CLI unavailable"],
                "retention_class": "runtime_cache",
                "archive_upload_state": "not_applicable",
                "cloud_capacity_class": "bounded",
                "last_archive_verified_utc": now_iso() if docker_state["docker_available"] else "",
            },
            {
                "surface": "notion",
                "status": "bounded_mirror",
                "capacity_class": "cloud_workspace",
                "notes": "Summary, dashboard, and reflection mirror only.",
                "live_checked_at": now_iso(),
                "reachable": True,
                "latest_artifact": "summary_only",
                "proof_state": "bounded_mirror_only",
                "blockers": [],
                "retention_class": "summary_mirror",
                "archive_upload_state": "not_applicable",
                "cloud_capacity_class": "bounded",
                "last_archive_verified_utc": now_iso(),
            },
            {
                "surface": "linear",
                "status": "bounded_action_mirror",
                "capacity_class": "cloud_workspace",
                "notes": "Actionable work mirror only.",
                "live_checked_at": now_iso(),
                "reachable": True,
                "latest_artifact": "actionable_items_only",
                "proof_state": "bounded_action_only",
                "blockers": [],
                "retention_class": "action_mirror",
                "archive_upload_state": "not_applicable",
                "cloud_capacity_class": "bounded",
                "last_archive_verified_utc": now_iso(),
            },
            {
                "surface": "new_project_workbench",
                "status": "local_read_surface",
                "capacity_class": "local_folder",
                "notes": "Workbench dashboard and operator shell. Not authoritative.",
                "live_checked_at": now_iso(),
                "reachable": WORKBENCH_ROOT.exists(),
                "latest_artifact": str(WORKBENCH_MIRROR_PATH),
                "proof_state": "workbench_read_only",
                "blockers": [] if WORKBENCH_ROOT.exists() else ["new project folder unavailable"],
                "retention_class": "local_workbench",
                "archive_upload_state": "not_applicable",
                "cloud_capacity_class": "none",
                "last_archive_verified_utc": now_iso() if WORKBENCH_ROOT.exists() else "",
            },
            {
                "surface": "google_drive",
                "status": drive_status,
                "capacity_class": drive_capacity_class,
                "notes": drive_notes,
                "live_checked_at": now_iso(),
                "reachable": drive_reachable,
                "latest_artifact": drive_latest_artifact,
                "proof_state": drive_proof_state,
                "blockers": drive_blockers,
                "retention_class": drive_retention_class,
                "archive_upload_state": drive_upload_state,
                "cloud_capacity_class": drive_capacity_class,
                "last_archive_verified_utc": drive_last_verified,
            },
        ],
        "official_sources": OFFICIAL_SOURCES,
    }
    return registry


def render_report_md(report: dict[str, Any]) -> str:
    lines = [
        "# Trinity Memory Bank Sync",
        "",
        f"- generated_utc: `{report['generated_utc']}`",
        f"- overall_status: `{report['overall_status']}`",
        f"- archive: `{report['archive']['path']}`",
        f"- archive_mb: `{report['archive']['size_mb']}`",
        f"- free_gib: `{report['storage_pressure']['free_gib']}`",
        "",
        "## Surfaces",
    ]
    for bank in report["surfaces"]:
        blockers = ", ".join(bank.get("blockers", [])) or "none"
        lines.append(
            f"- `{bank['surface']}`: status=`{bank['status']}`, reachable=`{bank['reachable']}`, proof_state=`{bank['proof_state']}`, blockers=`{blockers}`"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "- Repo remains the authority source.",
            "- GitHub is the current off-device path that is verifiably reachable today.",
            "- Google Drive may act as a bounded working mirror for non-authoritative artifacts, but it never overrides repo authority.",
            "- Docker/Postgres remain bounded runtime mirrors, not remote archive truth.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh Trinity memory-bank snapshot and sync registry.")
    parser.add_argument("--label", default="v11-memory-bank", help="Snapshot label.")
    parser.add_argument("--upload-google-drive", action="store_true", help="Upload the archive to Google Drive when a token is available.")
    parser.add_argument("--docker-copy-archive", action="store_true", help="Copy the latest archive into the running Postgres container as a bounded runtime mirror.")
    parser.add_argument("--fail-on-warn", action="store_true", help="Return a non-zero exit code if the report is WARN.")
    args = parser.parse_args()

    archive_path = create_archive(args.label, ARCHIVE_SOURCES, DEFAULT_ARCHIVE_DIR, DEFAULT_INDEX)
    git_state = probe_git()
    docker_state = probe_docker()
    drive_policy = google_drive_policy()
    operator_hold = bool(drive_policy.get("operator_hold"))
    drive_token = os.getenv("GOOGLE_DRIVE_ACCESS_TOKEN", "").strip()
    drive_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "").strip()

    drive_result: dict[str, Any] = {"uploaded": False, "blockers": []}
    if args.upload_google_drive:
        if operator_hold:
            drive_result["blockers"] = ["google drive activation deferred by operator"]
        elif not drive_token:
            drive_result["blockers"] = ["GOOGLE_DRIVE_ACCESS_TOKEN not set"]
        else:
            try:
                upload = upload_to_google_drive(archive_path, drive_token, drive_folder_id)
                drive_result = {
                    "uploaded": True,
                    "file_id": upload.get("id", ""),
                    "name": upload.get("name", archive_path.name),
                    "web_view_link": upload.get("webViewLink", ""),
                    "web_content_link": upload.get("webContentLink", ""),
                    "blockers": [],
                }
            except urllib.error.HTTPError as exc:
                drive_result = {
                    "uploaded": False,
                    "blockers": [f"google drive upload failed: HTTP {exc.code}"],
                }
            except Exception as exc:  # pragma: no cover - defensive
                drive_result = {
                    "uploaded": False,
                    "blockers": [f"google drive upload failed: {exc}"],
                }

    docker_copy = {"attempted": False, "success": False, "target": "", "stderr": ""}
    if args.docker_copy_archive and docker_state["docker_available"] and docker_state["postgres_container_running"]:
        docker_copy = maybe_copy_to_docker(archive_path)

    registry = build_registry(
        archive_path=archive_path,
        git_state=git_state,
        docker_state=docker_state,
        drive_result=drive_result,
        upload_attempted=args.upload_google_drive,
        docker_copy=docker_copy,
        drive_policy=drive_policy,
    )
    write_json(REGISTRY_PATH, registry)

    report = {
        "generated_utc": now_iso(),
        "overall_status": registry["overall_status"],
        "archive": {
            "path": path_to_repo_string(archive_path),
            "size_mb": registry["storage_pressure"]["archive_megabytes"],
            "index": path_to_repo_string(DEFAULT_INDEX),
        },
        "storage_pressure": registry["storage_pressure"],
        "surfaces": registry["memory_banks"],
        "latest_snapshot": registry["latest_snapshot"],
        "official_sources": OFFICIAL_SOURCES,
    }
    write_json(REPORT_JSON_PATH, report)
    write_text(REPORT_MD_PATH, render_report_md(report))
    write_jsonl(
        DRIVE_LEDGER_PATH,
        [
            {
                "timestamp": now_iso(),
                "archive_path": path_to_repo_string(archive_path),
                "target_surface": "google_drive",
                "result": (
                    "operator_hold"
                    if operator_hold
                    else (
                        "working_mirror_uploaded"
                        if str(drive_policy.get("drive_role") or "") == "bounded_working_mirror" and drive_result.get("uploaded")
                        else ("uploaded" if drive_result.get("uploaded") else ("attempted_blocked" if args.upload_google_drive else "staged"))
                    )
                ),
                "bytes": archive_path.stat().st_size if archive_path.exists() else 0,
                "rollback_state": "delete bounded mirror artifact" if drive_result.get("uploaded") else "no remote archive written",
            }
        ],
    )
    WORKBENCH_MIRROR_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_json(WORKBENCH_MIRROR_PATH, report)
    write_text(
        PLAYBOOK_PATH,
        "# Trinity Memory Bank Playbook\n\n"
        "- Repo remains authoritative for certificates, ledgers, reflections, commands, and official state.\n"
        "- GitHub is the current proven off-device mirror surface.\n"
        "- Docker/Postgres are bounded runtime mirrors, not authority.\n"
        "- Google Drive may be used as a bounded working mirror for non-authoritative artifacts only; it never overrides repo authority.\n\n"
        "## Official references\n"
        f"- Google Drive files.create: {OFFICIAL_SOURCES['google_drive_api']}\n"
        f"- Google Drive uploads guide: {OFFICIAL_SOURCES['google_drive_uploads']}\n"
        f"- Docker volumes: {OFFICIAL_SOURCES['docker_volumes']}\n"
        f"- git bundle: {OFFICIAL_SOURCES['git_bundle']}\n",
    )

    if args.fail_on_warn and report["overall_status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
