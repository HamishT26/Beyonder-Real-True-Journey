#!/usr/bin/env python3
"""Aurelis Reflection and Memory Update System.

Stores message-level reflection entries in JSONL + Markdown for continuity.
If `--nzdt-context` is omitted, context is derived from Aurelis Atomic NZ Clock.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
JSONL_PATH = ROOT / "docs" / "aurelis-memory-log.jsonl"
MD_PATH = ROOT / "docs" / "aurelis-memory-log.md"
CLOCK_STATE = ROOT / "docs" / "aurelis-nz-clock-state.json"


@dataclass
class MemoryEntry:
    timestamp_utc: str
    nzdt_context: str
    role: str
    user_message: str
    assistant_reflection: str
    progress_snapshot: str
    next_step: str


def derive_nzdt_context() -> str:
    nz_now = datetime.now(timezone.utc).astimezone(ZoneInfo("Pacific/Auckland"))
    if not CLOCK_STATE.exists():
        return nz_now.strftime("%I:%M%p NZDT %a %d %b %Y")

    state = json.loads(CLOCK_STATE.read_text())
    session = state.get("session_name", "session")
    start_utc = state.get("session_start_utc")
    if not start_utc:
        return nz_now.strftime("%I:%M%p NZDT %a %d %b %Y")

    start = datetime.fromisoformat(start_utc)
    mins = int((datetime.now(timezone.utc) - start).total_seconds() // 60)
    return f"{nz_now.strftime('%I:%M%p NZDT %a %d %b %Y')} | session={session} | +{mins}m"


def run_zip_archive(
    label: str,
    encrypt_passphrase: str = "",
    keep_last: int = 0,
    prune_delete_files: bool = False,
) -> None:
    cmd = [
        "python3",
        "scripts/trinity_zip_memory_converter.py",
        "archive",
        "--label",
        label,
    ]
    if encrypt_passphrase:
        cmd.extend(["--encrypt-passphrase", encrypt_passphrase])

    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode == 0:
        if proc.stdout.strip():
            print(proc.stdout.strip())
    else:
        err = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        print(f"[warn] zip archive step failed: {err.strip()}")
        return

    if keep_last > 0:
        prune_cmd = [
            "python3",
            "scripts/trinity_zip_memory_converter.py",
            "prune",
            "--keep-last",
            str(keep_last),
            "--label-contains",
            label,
        ]
        if prune_delete_files:
            prune_cmd.append("--delete-files")

        prune_proc = subprocess.run(prune_cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        if prune_proc.returncode == 0:
            if prune_proc.stdout.strip():
                print(prune_proc.stdout.strip())
        else:
            err = (prune_proc.stdout or "") + ("\n" + prune_proc.stderr if prune_proc.stderr else "")
            print(f"[warn] zip prune step failed: {err.strip()}")


def append_markdown(entry: MemoryEntry) -> None:
    if not MD_PATH.exists():
        MD_PATH.write_text("# Aurelis Memory Log\n\n")
    with MD_PATH.open("a") as f:
        f.write(f"## {entry.timestamp_utc} ({entry.nzdt_context})\n")
        f.write(f"- role: **{entry.role}**\n")
        f.write(f"- user_message: {entry.user_message}\n")
        f.write(f"- assistant_reflection: {entry.assistant_reflection}\n")
        f.write(f"- progress_snapshot: {entry.progress_snapshot}\n")
        f.write(f"- next_step: {entry.next_step}\n\n")


def main() -> None:
    p = argparse.ArgumentParser(description="Append an Aurelis memory/reflection entry")
    p.add_argument("--nzdt-context", help="Optional NZ context; auto-derived from NZ clock if omitted")
    p.add_argument("--role", default="assistant")
    p.add_argument("--user-message", required=True)
    p.add_argument("--assistant-reflection", required=True)
    p.add_argument("--progress-snapshot", required=True)
    p.add_argument("--next-step", required=True)
    p.add_argument("--skip-zip-archive", action="store_true", help="Skip automatic zip archive snapshot for this update")
    p.add_argument("--zip-encrypt-passphrase", default="", help="Optional passphrase for encrypted .ezip archive snapshots")
    p.add_argument(
        "--zip-keep-last",
        type=int,
        default=0,
        help="If >0, prune memory-update archive index entries to keep only the latest N entries after write",
    )
    p.add_argument(
        "--zip-prune-delete-files",
        action="store_true",
        help="When pruning, also delete removed archive files from disk",
    )
    args = p.parse_args()

    entry = MemoryEntry(
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        nzdt_context=args.nzdt_context or derive_nzdt_context(),
        role=args.role,
        user_message=args.user_message,
        assistant_reflection=args.assistant_reflection,
        progress_snapshot=args.progress_snapshot,
        next_step=args.next_step,
    )

    JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSONL_PATH.open("a") as f:
        f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    append_markdown(entry)
    print(f"Updated {JSONL_PATH} and {MD_PATH}")

    if not args.skip_zip_archive:
        run_zip_archive(
            label="memory-update",
            encrypt_passphrase=args.zip_encrypt_passphrase,
            keep_last=args.zip_keep_last,
            prune_delete_files=args.zip_prune_delete_files,
        )


if __name__ == "__main__":
    main()
