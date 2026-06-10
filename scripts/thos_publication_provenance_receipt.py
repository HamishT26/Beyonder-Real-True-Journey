#!/usr/bin/env python3
"""Write compact provenance receipts for curated THOS phase artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_text(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unavailable"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_file(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise SystemExit(f"refusing non-repo-relative path: {value}")
    return candidate


def subject_row(value: str) -> dict[str, Any]:
    rel = relative_file(value)
    path = ROOT / rel
    if not path.exists() or not path.is_file():
        raise SystemExit(f"subject file missing: {value}")
    return {
        "path": rel.as_posix(),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
    }


def material_row(value: str) -> dict[str, Any]:
    rel = relative_file(value)
    path = ROOT / rel
    row: dict[str, Any] = {
        "path": rel.as_posix(),
        "exists": path.exists() and path.is_file(),
    }
    if row["exists"]:
        row["sha256"] = sha256_file(path)
        row["bytes"] = path.stat().st_size
    return row


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Publication Provenance Receipt",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- local_head: `{payload['git']['local_head']}`",
        f"- remote_head: `{payload['git']['remote_head']}`",
        f"- drift: `{payload['git']['drift']}`",
        "",
        "## Subjects",
    ]
    for row in payload["subjects"]:
        lines.append(f"- `{row['path']}` bytes `{row['bytes']}` sha256 `{row['sha256']}`")
    lines.append("")
    lines.append("## Materials")
    for row in payload["materials"]:
        if row.get("exists"):
            lines.append(f"- `{row['path']}` bytes `{row['bytes']}` sha256 `{row['sha256']}`")
        else:
            lines.append(f"- `{row['path']}` missing at receipt time")
    lines.extend(
        [
            "",
            "This receipt records repo-relative file subjects and material hashes only. It does not publish raw lane text, raw transport, session streams, image captures, credentials, or private dumps.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--subject", action="append", required=True)
    parser.add_argument("--material", action="append", default=[])
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    subjects = [subject_row(value) for value in args.subject]
    materials = [material_row(value) for value in args.material]
    payload = {
        "artifact_type": "publication_provenance_receipt",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_PUBLICATION_PROVENANCE_READY",
        "subjects": subjects,
        "materials": materials,
        "git": {
            "local_head": git_text(["rev-parse", "HEAD"]),
            "remote_head": git_text(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"]),
            "drift": git_text(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"]),
        },
        "claim_boundary": {
            "repo_relative_paths_only": True,
            "raw_lane_text_published": False,
            "raw_transport_published": False,
            "session_streams_published": False,
            "credentials_published": False,
            "external_account_mutation": False,
            "gmut_gate_state": "all_gmut_gates_remain_open",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "subjects": len(subjects)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
