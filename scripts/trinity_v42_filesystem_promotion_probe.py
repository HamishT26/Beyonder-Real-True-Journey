#!/usr/bin/env python3
"""Gate filesystem promotion on real V42 WSL/Codex proof instead of shell-only reachability."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from trinity_v42_common import LOCAL_RUNTIME_DIR, REPO_MOUNT, ROOT, now_iso, read_json, safe_run, write_json, write_text

OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-filesystem-promotion-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v42-filesystem-promotion-proof-v1.md"
WSL_PROBE_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-wsl-codex-probe-v1.json"
ROUNDTRIP_FILE = ROOT / ".local-runtime" / "v42" / "wsl-filesystem-roundtrip.txt"


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 Filesystem Promotion Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Filesystem promotion state: `{payload['filesystem_promotion_state']}`",
        f"- Repo roundtrip state: `{payload['repo_roundtrip_state']}`",
        f"- Proof publication state: `{payload['proof_publication_state']}`",
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
    parser = argparse.ArgumentParser(description="Probe whether filesystem promotion can be honestly unblocked in V42.")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    LOCAL_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    wsl_probe = read_json(WSL_PROBE_JSON)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "overall_status": "WARN",
        "filesystem_promotion_state": "blocked",
        "repo_roundtrip_state": "pending",
        "proof_publication_state": "pending",
        "completed_steps": [],
        "blockers": [],
        "wsl_probe_path": str(WSL_PROBE_JSON.relative_to(ROOT)).replace("\\", "/"),
    }

    if not wsl_probe:
        payload["overall_status"] = "FAIL"
        payload["repo_roundtrip_state"] = "blocked_missing_wsl_probe"
        payload["proof_publication_state"] = "blocked_missing_wsl_probe"
        payload["blockers"].append("The V42 filesystem probe requires the published WSL/Codex probe as its baseline evidence.")
        write_json(Path(args.output_json), payload)
        write_text(Path(args.output_md), markdown(payload))
        return 1

    roundtrip_marker = f"V42_WSL_FILESYSTEM_OK::{now_iso()}"
    write_proc = safe_run(
        [
            "wsl.exe",
            "-d",
            "Ubuntu",
            "--",
            "bash",
            "-lc",
            f"printf '%s' '{roundtrip_marker}' > {REPO_MOUNT}/.local-runtime/v42/wsl-filesystem-roundtrip.txt",
        ],
        timeout=60,
    )
    if write_proc.returncode == 0 and ROUNDTRIP_FILE.exists() and ROUNDTRIP_FILE.read_text(encoding="utf-8") == roundtrip_marker:
        payload["repo_roundtrip_state"] = "wsl_to_windows_file_roundtrip_verified"
        payload["completed_steps"].append("wsl_repo_write_roundtrip_verified")
    else:
        payload["repo_roundtrip_state"] = "wsl_to_windows_file_roundtrip_blocked"
        payload["blockers"].append("A bounded WSL-originated write to the authoritative repo could not be verified from Windows.")

    publication_marker = {
        "generated_utc": now_iso(),
        "marker": roundtrip_marker,
        "source": "v42_filesystem_promotion_probe",
        "roundtrip_file": str(ROUNDTRIP_FILE.relative_to(ROOT)).replace("\\", "/"),
    }
    publication_path = ROOT / "docs" / "trinity-live-traces" / "v42-filesystem-publication-marker-v1.json"
    write_json(publication_path, publication_marker)
    if publication_path.exists():
        payload["proof_publication_state"] = "windows_publication_verified"
        payload["completed_steps"].append("windows_publication_cycle_verified")
    else:
        payload["proof_publication_state"] = "windows_publication_blocked"
        payload["blockers"].append("The bounded filesystem publication marker was not written to the repo proof surface.")

    selector_state = str(wsl_probe.get("wsl_codex_selector_state") or "")
    if selector_state != "cli_wsl_entrypoint_verified":
        payload["filesystem_promotion_state"] = "blocked"
        payload["blockers"].append("Filesystem promotion remains blocked because the Codex desktop WSL selector or equivalent full binding proof is still unresolved.")
    elif payload["repo_roundtrip_state"] == "wsl_to_windows_file_roundtrip_verified" and payload["proof_publication_state"] == "windows_publication_verified":
        payload["filesystem_promotion_state"] = "unblocked"
        payload["overall_status"] = "PASS"
        payload["completed_steps"].append("filesystem_promotion_gate_verified")

    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
